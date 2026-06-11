# Language Detection Algorithms

This package bundles five OVOS language-detector plugins, each wrapping a different
classic algorithm, plus a `VotingLangDetectPlugin` that combines them. The sections
below describe each algorithm's origins, design, strengths, and how it holds up today.

---

## CLD2 — Compact Language Detector 2

**Plugin entry-point:** `ovos-lang-detector-plugin-cld2`  
**Class:** `Pycld2Detector` (`ovos_lang_detector_classics_plugin.neon_cld2`)  
**Python package:** `pycld2`  
**Languages supported:** ~80

### History

CLD2 was written at Google around 2011 and open-sourced in 2013. It was the production
language detector behind Chrome and Google Translate for several years. The algorithm
is a **Naïve Bayes classifier over byte n-grams (quadgrams)**. Training data came from
web pages whose language was known from HTTP headers; the model was distilled into a
compact trie that fits in ~1 MB of memory.

### How it works

1. The input text is Unicode-normalised and split into overlapping 4-byte sequences.
2. Each quadgram votes for one or more languages according to a pre-trained lookup
   table.
3. Votes are accumulated per language; the top result is returned with a reliability
   score.
4. CLD2 can optionally accept **hint signals** — a top-level domain, an HTTP
   `Content-Language` header, or an explicit language hint — which boost the prior
   probability of one language before voting begins. This is exposed in
   `Pycld2Detector` via `self.boost` / `self.hint_language`.

### Strengths

- **Extremely fast** — nanoseconds per short string, no model loading time.
- **Tiny footprint** — suitable for embedded or memory-constrained environments.
- **Multi-language detection** — can return up to three languages with their
  byte-fraction share; useful for mixed-language texts.
- **Reliable for longer texts** — accuracy is high once there are 200+ bytes.

### Weaknesses in the modern era

- **Short text accuracy is poor.** Fewer than ~20 characters often produce wrong
  or `"un"` (unknown) results. CLD2 was designed for web-page bodies, not tweets or
  voice utterances.
- **Language coverage is dated.** ~80 languages; many low-resource languages are
  absent.
- **Unmaintained.** The C++ library has not had a significant update since 2015; the
  Python binding `pycld2` is a thin wrapper with occasional packaging issues (notably
  the `AttributeError: 'boost'` crash on some platforms that motivated the exception
  isolation work in this repo).
- **No probabilistic guarantee.** Confidence scores are byte-fractions, not calibrated
  probabilities.

### When to use

Good as a **secondary voter** for texts > 50 characters where speed is critical or
memory is scarce. Its hint mechanism makes it uniquely useful when metadata about the
input's likely language is available. Weight it below 1.0 in the voting ensemble (the
default is 0.8) to dampen its short-text noise.

---

## CLD3 — Compact Language Detector 3

**Plugin entry-point:** `ovos-lang-detector-plugin-cld3`  
**Class:** `Cld3Detector` (`ovos_lang_detector_classics_plugin.cld3`)  
**Python package:** `gcld3`  
**Languages supported:** ~107

### History

CLD3 was developed at Google around 2015 and released publicly in 2017. It replaced
CLD2 in Chrome. The algorithm moved from n-gram Naïve Bayes to a **small feed-forward
neural network** trained on character n-gram embeddings. The `gcld3` Python package
wraps the C++ implementation via protobuf.

### How it works

1. The input text is tokenised into a character n-gram vocabulary (unigrams through
   4-grams, Unicode-normalised).
2. Each n-gram is hashed to a bucket; embeddings for all buckets are summed and
   averaged into a fixed-size feature vector.
3. A two-layer feed-forward network maps the feature vector to per-language logits.
4. Softmax produces probabilities across 107 language labels.
5. `FindTopNMostFreqLangs` returns the top-N labels; results labelled `"und"` (unknown)
   are filtered out in this plugin.

The model is ~2 MB and is bundled with the `gcld3` package, so there is no download
step.

### Strengths

- **Better short-text accuracy than CLD2** — the neural approach generalises more
  robustly to fewer tokens.
- **More languages than CLD2** — 107 vs ~80.
- **Still very fast** — inference is on the order of microseconds on modern hardware.
- **No external state** — the model is fully embedded; no internet access or
  configuration required.

### Weaknesses in the modern era

- **Inferior to transformer models** — CLD3 accuracy on ambiguous short texts
  (< 20 tokens) is significantly below modern approaches like LangDetect+fastText.
- **Not actively maintained.** The `gcld3` Python binding is fragile; it has broken
  on several Python/NumPy version combinations and may fail to build on some
  platforms.
- **Fixed vocabulary.** Character n-gram hashing means out-of-vocabulary tokens still
  contribute noise; no contextual understanding.
- **Language set mismatch.** The 107-language list differs from ISO 639-1 in several
  places; codes like `"zh-Hant"` appear instead of `"zh"`, which can cause issues
  downstream.

### When to use

A solid upgrade over CLD2 when the extra memory and slightly longer import time are
acceptable. Useful as a secondary voter alongside `langdetect` or `fastlang`. In the
voting ensemble, a weight of 0.8 is reasonable.

---

## langdetect

**Plugin entry-point:** `ovos-lang-detector-plugin-langdetect`  
**Class:** `LangDetectDetector` (`ovos_lang_detector_classics_plugin.neon_langdetect`)  
**Python package:** `langdetect`  
**Languages supported:** 55

### History

`langdetect` is a Python port of Nakatani Shuyo's **language-detection Java library**
(2010), which implements the algorithm described in:

> Shuyo Nakatani, "Language Detection Library for Java", 2010.  
> Nakatani & Mori, "A Practical Approach to Language Detection using Character N-grams", 2012.

The algorithm uses a **Bayesian classifier over character n-gram profiles**. Language
profiles were built from Wikipedia dumps; each profile stores the relative frequency of
1–3 character n-grams in that language.

### How it works

1. The input is stripped of non-alphabetic characters and split into n-grams (length 1–3).
2. Each n-gram frequency is compared against all stored language profiles using a
   Bayesian update (each profile contributes a log-likelihood increment).
3. The algorithm draws multiple random samples from the text and averages posterior
   estimates to reduce variance — a Monte-Carlo approach that makes the result
   **non-deterministic by default**.
4. `detect()` returns the highest-probability language code; `detect_langs()` returns
   a ranked list of `(lang, probability)` pairs.

### Strengths

- **Well-tested and widely deployed.** The Java original and its ports have been used
  in production for 15 years.
- **Good accuracy on mid-length texts (50–500 chars).**
- **Probabilistic output** — confidence values from `detect_langs` are a proper
  distribution that sums to 1.
- **55 languages including several CJK and Indic scripts** that CLD2/CLD3 handle
  poorly.

### Weaknesses in the modern era

- **Non-determinism.** The Monte-Carlo sampling means the same text can yield
  different results across runs. This is usually harmless in a voting ensemble but can
  confuse debugging. A seed can be set globally but there is no per-call API.
- **Limited language set** — 55 languages; no Arabic, no low-resource languages.
- **Short text fragility** — texts under ~20 characters produce low-confidence,
  unreliable results.
- **Slow relative to CLD2/CLD3** — profiling shows 1–5 ms per call vs < 1 ms for the
  compiled alternatives.
- **Wikipedia-biased profiles** — formal register text is detected better than spoken
  or informal language, which is a problem for voice assistant utterances.

### When to use

Best for longer, more formal texts where calibrated probability distributions matter.
In the voting ensemble it contributes a useful independent signal from CLD2/CLD3
because its n-gram profiles and training corpus are different. Default weight 1.0.

---

## fastlang

**Plugin entry-point:** `ovos-lang-detector-plugin-fastlang`  
**Class:** `FastLangDetector` (`ovos_lang_detector_classics_plugin.neon_fastlang`)  
**Python package:** `fastlang`  
**Languages supported:** 176

### History

`fastlang` is a Python wrapper around **fastText's language identification model**,
published by Facebook Research in 2017:

> Joulin et al., "Bag of Tricks for Efficient Text Classification", EACL 2017.  
> Joulin et al., "FastText.zip: Compressing text classification models", ICLR 2017.

The `lid.176.ftz` model — which `fastlang` bundles — is a compressed (~917 KB)
character n-gram + subword fastText classifier trained on Wikipedia, Tatoeba, and SETimes
covering **176 languages**.

### How it works

1. Text is lowercased and tokenised into words; each word is decomposed into
   character n-grams (length 2–4) and subwords.
2. Each n-gram/subword is hashed to a shared embedding table; embeddings are summed
   into a sentence vector.
3. A linear classifier maps the sentence vector to 176 language logits.
4. Softmax scores are returned as the probability distribution.

fastText's key innovation is the **subword hash trick**: out-of-vocabulary words still
contribute information via their character n-grams, making the model robust to
spelling variants, inflected forms, and informal text.

### Strengths

- **Widest language coverage** — 176 languages, including many low-resource languages
  absent from all other detectors here.
- **Best short-text accuracy** in this ensemble. FastText's subword representations
  work well on 5–15 token texts typical of voice utterances.
- **Fast** — the compressed model infers in < 1 ms.
- **Good on informal and spoken language** — subword representations handle
  abbreviations, code-switching, and typos better than n-gram profiles.

### Weaknesses in the modern era

- **fastText is no longer the state of the art** — transformer-based models (e.g.
  `lingua`, `langdetect-rs`, GlotLID) outperform it on ambiguous short texts.
- **Language codes use fastText's `__label__xx` format** internally; `fastlang` strips
  this but the underlying model may return codes that differ from ISO 639-1 (e.g.,
  `"sh"` for Serbo-Croatian instead of separate `"sr"`/`"hr"`).
- **One-shot output** — the returned probabilities are from a single-pass linear
  classifier, which can be overconfident on ambiguous texts.

### When to use

The **highest-value single detector** in the ensemble for short voice utterances.
Should always be included and weighted at 1.0. If only one detector can be installed,
make it this one.

---

## VotingLangDetectPlugin — Ensemble Voting

**Plugin entry-point:** `ovos-lang-detector-plugin-voter`  
**Class:** `VotingLangDetectPlugin` (`ovos_lang_detector_classics_plugin`)

### Motivation

Each classic algorithm has systematic failure modes on different input types. CLD2
fails on short texts; `langdetect` is non-deterministic and misses Arabic; CLD3 has
packaging fragility; fastlang is overconfident on ambiguous single-word inputs. An
ensemble that **averages weighted predictions** is consistently more robust than any
single detector, at the cost of loading multiple models.

### How it works

```
detect_probs(text)
  for each voter:
    try:
      probs = voter.detect_probs(text)      # {lang_code: float, ...}
      for lang, prob in probs:
        counts[lang].append(prob * weight)
    except Exception:
      LOG.debug(...)                        # one bad detector never aborts the round

  if use_max:
    result[lang] = max(counts[lang])        # conservative: take the strongest signal
  else:
    result[lang] = mean(counts[lang])       # default: average across contributing voters
```

`detect(text)` is `argmax(detect_probs(text))`.

The **exception isolation** (added in this repo) means a detector that crashes — e.g.
CLD2's `AttributeError: 'boost'` on some platforms — silently drops out for that
utterance rather than aborting the whole voting round.

### Configuration

```yaml
# mycroft.conf / ovos.conf  (under the plugin's section)
lang_detection:
  module: ovos-lang-detector-plugin-voter
  ovos-lang-detector-plugin-voter:
    weights:
      ovos-lang-detector-plugin-cld2: 0.8
      ovos-lang-detector-plugin-langdetect: 1.0
      ovos-lang-detector-plugin-fastlang: 1.0
    use_max: false   # true = take max per lang instead of mean
```

Omitting a plugin from `weights` excludes it. CLD3 is not in the default weights
because its Python packaging is fragile; add it manually if it installs cleanly on your
platform.

### Aggregation modes

| `use_max` | Formula | When to prefer |
|-----------|---------|----------------|
| `false` (default) | `mean(weighted_votes)` | Most texts; spreads confidence across voters; prevents a single overconfident detector from dominating |
| `true` | `max(weighted_votes)` | Short utterances where you want the most decisive signal; useful when fastlang is the only voter that fires |

### Recommended weight presets

**Voice assistant (short utterances, 1–15 words):**

```yaml
weights:
  ovos-lang-detector-plugin-fastlang: 1.0
  ovos-lang-detector-plugin-cld2: 0.5
```

**Document / long-form text:**

```yaml
weights:
  ovos-lang-detector-plugin-langdetect: 1.0
  ovos-lang-detector-plugin-cld2: 1.0
  ovos-lang-detector-plugin-cld3: 0.8
```

**Maximum coverage (install all optional deps):**

```yaml
weights:
  ovos-lang-detector-plugin-fastlang: 1.0
  ovos-lang-detector-plugin-langdetect: 1.0
  ovos-lang-detector-plugin-cld2: 0.8
  ovos-lang-detector-plugin-cld3: 0.8
use_max: false
```

---

## Algorithm Comparison

| Property | CLD2 | CLD3 | langdetect | fastlang |
|---|---|---|---|---|
| Algorithm | Naïve Bayes, byte quadgrams | Feed-forward NN, char n-grams | Bayesian, char n-gram profiles | fastText linear, subword |
| Origin | Google, 2011 | Google, 2015 | Nakatani Shuyo, 2010 | Facebook Research, 2017 |
| Languages | ~80 | ~107 | 55 | 176 |
| Model size | ~1 MB (compiled) | ~2 MB | ~3 MB | ~1 MB (compressed) |
| Short text (< 20 chars) | Poor | Fair | Poor | Good |
| Mid text (20–200 chars) | Fair | Good | Good | Good |
| Long text (> 200 chars) | Good | Good | Good | Good |
| Informal / spoken text | Poor | Fair | Poor | Good |
| Deterministic | Yes | Yes | No (Monte Carlo) | Yes |
| Low-resource languages | No | Limited | No | Yes |
| Hint/prior injection | Yes | No | No | No |
| Runtime fragility | Occasional | Packaging | None | None |

---

## Developer Reference

### Adding a new backend

1. Create a new module under `ovos_lang_detector_classics_plugin/`, subclassing
   `ovos_plugin_manager.templates.language.LanguageDetector`.
2. Implement `detect(text: str) -> str` and `detect_probs(text: str) -> dict[str, float]`.
3. Register the entry-point in `pyproject.toml` under `[project.entry-points."neon.plugin.lang.detect"]`.
4. Optionally add it to the `VotingLangDetectPlugin` default weights.

Minimal skeleton:

```python
from ovos_plugin_manager.templates.language import LanguageDetector
from ovos_utils import classproperty

class MyDetector(LanguageDetector):
    def detect(self, text: str) -> str:
        ...

    def detect_probs(self, text: str) -> dict:
        # return {lang_code: float} — values need not sum to 1
        ...

    @classproperty
    def available_languages(cls):
        return {"en", "pt", ...}
```

### Using the voter programmatically

```python
from ovos_lang_detector_classics_plugin import VotingLangDetectPlugin

detector = VotingLangDetectPlugin(config={
    "weights": {
        "ovos-lang-detector-plugin-fastlang": 1.0,
        "ovos-lang-detector-plugin-langdetect": 1.0,
    }
})

print(detector.detect("hello world"))          # "en"
print(detector.detect_probs("olá mundo"))      # {"pt": 0.94, "es": 0.06, ...}
```

### Using a single backend directly

```python
from ovos_lang_detector_classics_plugin.neon_fastlang import FastLangDetector
from ovos_lang_detector_classics_plugin.neon_cld2 import Pycld2Detector
from ovos_lang_detector_classics_plugin.neon_langdetect import LangDetectDetector
from ovos_lang_detector_classics_plugin.cld3 import Cld3Detector

d = FastLangDetector()
print(d.detect("bonjour le monde"))            # "fr"
print(d.detect_probs("bonjour le monde"))      # {"fr": 0.99, ...}
```

### Exception isolation

`VotingLangDetectPlugin.detect_probs` wraps each voter call in `try/except`. A
detector that raises (e.g. CLD2's `AttributeError: 'boost'` on certain platforms) is
skipped with a `LOG.debug` message; the remaining voters still contribute. If **all**
voters raise, the method returns `{}` — callers should handle an empty dict or a
`RuntimeError` from the caller's `detect()`.

### Optional dependencies

The backend libraries are all optional; the voter plugin will raise `RuntimeError` on
init if a configured backend cannot be loaded. Install only what you need:

```bash
pip install ovos-lang-detector-classics-plugin           # core only (voter + imports)
pip install "ovos-lang-detector-classics-plugin[all]"    # + pycld2, gcld3, langdetect, fastlang
pip install pycld2 langdetect fastlang                   # pick individually
```

`gcld3` is not in the `[all]` extra because its build is brittle on some
platforms (requires protobuf headers). Install it separately after verifying
it builds on your system:

```bash
pip install gcld3
```
