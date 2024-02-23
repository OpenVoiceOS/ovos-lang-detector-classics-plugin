# from https://github.com/NeonGeckoCom/neon-lang-plugin-fastlang
from ovos_plugin_manager.templates.language import LanguageDetector
from fastlang import fastlang


class FastLangDetector(LanguageDetector):

    def detect(self, text):
        return fastlang(text)["lang"]

    def detect_probs(self, text):
        return fastlang(text)["probabilities"]
