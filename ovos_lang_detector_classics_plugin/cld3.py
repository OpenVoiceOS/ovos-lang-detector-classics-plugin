from ovos_plugin_manager.templates.language import LanguageDetector
import gcld3


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

