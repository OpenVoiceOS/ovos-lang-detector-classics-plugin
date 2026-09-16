import gcld3
from ovos_plugin_manager.templates.language import LanguageDetector
from ovos_utils import classproperty


class Cld3Detector(LanguageDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)

    def detect(self, text):
        result = self.detector.FindLanguage(text=text)
        return result.language if result.language != "und" else None

    def detect_probs(self, text):
        results = self.detector.FindTopNMostFreqLangs(text=text, num_langs=3)
        return {r.language: r.probability for r in results if r.language != "und"}

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
