# from https://github.com/NeonGeckoCom/neon-lang-plugin-langdetect
from ovos_plugin_manager.templates.language import LanguageDetector
from langdetect import detect, detect_langs


class LangDetectDetector(LanguageDetector):
    def detect(self, text):
        return detect(text)

    def detect_probs(self, text):
        langs = {}
        for lang in detect_langs(text):
            langs[lang.lang] = lang.prob
        return langs