# Lang Classifier Classics

Provides plugins for the following packages:

- https://github.com/google/cld3 - CLD3 is a neural network model for language identification
- https://github.com/aboSamoor/pycld2 - CLD2 is a Naïve Bayesian classifier, detects over 80 languages
- https://github.com/kootenpv/fastlang - Built upon the nltk stopwords, without depending on nltk itself.
- https://github.com/Mimino666/langdetect - Detect language of a text using naive Bayesian filter

Additionally, a "voter" plugin is provided, it will use other plugins and average predictions, each model compensates for the other bias balancing each other out better and increasing accuracy

To use use the plugins above, `pip install ovos-lang-detector-plugin-voter[all]`, if you dont need the plugins except for voter plugin skip the `[all]` flag

> **NOTE**: The voter plugin can be used with **any** lang detect plugin, not only the ones above


## Configuration


in `mycroft.conf` 

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
## Credits

bundled package plugins originally from @NeonGeckoCom but never published
