# from https://github.com/NeonGeckoCom/neon-lang-plugin-langdetect
from langdetect import detect, detect_langs
from ovos_plugin_manager.templates.language import LanguageDetector
from ovos_utils import classproperty


class LangDetectDetector(LanguageDetector):
    def detect(self, text):
        return detect(text)

    def detect_probs(self, text):
        langs = {}
        for lang in detect_langs(text):
            langs[lang.lang] = lang.prob
        return langs

    @classproperty
    def available_languages(cls):
        """
        Return languages supported by this detector implementation in this state.
        This should be a set of languages this detector is capable of recognizing.
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            Set[str]: A set of language codes supported by this detector.
        """
        return set()  # TODO
