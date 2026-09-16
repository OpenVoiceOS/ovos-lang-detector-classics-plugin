# Lang Classifier Classics

This package provides OVOS language-detection plugins for four classic algorithms:

- [google/cld3](https://github.com/google/cld3): CLD3 is a neural network model for language identification.
- [aboSamoor/pycld2](https://github.com/aboSamoor/pycld2): CLD2 is a Naive Bayesian classifier. It detects over 80 languages.
- [kootenpv/fastlang](https://github.com/kootenpv/fastlang): built on the NLTK stopword lists, without depending on NLTK itself.
- [Mimino666/langdetect](https://github.com/Mimino666/langdetect): detects the language of a text with a naive Bayesian filter.

The package also provides a `VotingLangDetectPlugin`. This plugin runs the other plugins and averages their predictions. Each model has a different bias, so the average is usually more accurate than any single model. See [docs/algorithms.md](docs/algorithms.md) for details on each algorithm and the voting logic.

To use the plugins above, run `pip install ovos-lang-detector-classics-plugin[all]`. If you only need the voter plugin, skip the `[all]` flag.

> **NOTE**: The voter plugin works with any lang-detect plugin, not only the ones listed above.

## Configuration

Add this to `mycroft.conf`:

```javascript
  "language": {
    "detection_module": "ovos-lang-detector-plugin-voter",
    
    "ovos-lang-detector-plugin-voter": {
        "weights": {
            "ovos-lang-detector-plugin-cld3": 0.8,
            "ovos-lang-detector-plugin-cld2": 0.8,
            "ovos-lang-detector-plugin-lingua-podre": 1.0,
            "ovos-lang-detector-plugin-langdetect": 1.0,
            "ovos-lang-detector-plugin-fastlang": 1.0,
        }
    }
    
  },
```

## Usage

```python
weights = {
    "ovos-lang-detector-plugin-cld3": 0.8,
    "ovos-lang-detector-plugin-cld2": 0.8,
    "ovos-lang-detector-plugin-lingua-podre": 1.0,
    "ovos-lang-detector-plugin-langdetect": 1.0,
    "ovos-lang-detector-plugin-fastlang": 1.0,
}
p = VotingLangDetectPlugin(config={"weights": weights})

for utt in ["hello world",
            "olá mundo",
            "hola mundo",
            "once upon a time there was a voice assistant",
            "era uma vez um assistente de voz"]:
    print(p.detect(utt))
```

## Related projects

- [OpenVoiceOS/ovos-plugin-manager](https://github.com/OpenVoiceOS/ovos-plugin-manager): defines the `LanguageDetector` base class these plugins implement.
- [OpenVoiceOS/ovos-translate-server](https://github.com/OpenVoiceOS/ovos-translate-server): a server that exposes language detection and translation plugins over HTTP.

## Credits

The bundled plugins originally came from [NeonGeckoCom](https://github.com/NeonGeckoCom) but were never published on their own.

## License

Apache-2.0
