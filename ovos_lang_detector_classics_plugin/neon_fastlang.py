# from https://github.com/NeonGeckoCom/neon-lang-plugin-fastlang
from fastlang import fastlang
from ovos_plugin_manager.templates.language import LanguageDetector
from ovos_utils import classproperty


class FastLangDetector(LanguageDetector):

    def detect(self, text):
        return fastlang(text)["lang"]

    def detect_probs(self, text):
        return fastlang(text)["probabilities"]

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
