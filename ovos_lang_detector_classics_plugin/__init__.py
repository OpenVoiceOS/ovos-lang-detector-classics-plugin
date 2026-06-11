from ovos_plugin_manager.language import load_lang_detect_plugin
from ovos_plugin_manager.templates.language import LanguageDetector
from ovos_utils import classproperty
from ovos_utils.log import LOG
from typing import Set


class VotingLangDetectPlugin(LanguageDetector):
    """language detector that uses several other plugins and averages their predictions"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weights = self.config.get("weights", {
            "ovos-lang-detector-plugin-cld2": 0.8,
            "ovos-lang-detector-plugin-langdetect": 1.0,
            "ovos-lang-detector-plugin-fastlang": 1.0,
        })
        if not self.weights:
            raise ValueError("'weights' dict must contain lang detection plugins as keys "
                             "and a float between 0 and 1 as value")
        self.voters = self.load_plugins()

    def load_plugins(self):
        plugs = {}
        for plug_name in self.weights:
            try:
                plugs[plug_name] = load_lang_detect_plugin(plug_name)()
            except:
                raise RuntimeError(f"Failed to load {plug_name}")
        return plugs

    def detect(self, text):
        preds = self.detect_probs(text)
        return max(preds, key=lambda k: preds.get(k, 0))

    def detect_probs(self, text):
        counts = {}
        for plug, voter in self.voters.items():
            try:
                for k, v in voter.detect_probs(text).items():
                    if k not in counts:
                        counts[k] = []
                    counts[k].append(v * self.weights[plug])
            except Exception as e:
                LOG.debug(f"Lang detector '{plug}' raised an exception, skipping: {e}")
        if self.config.get("use_max"):
            counts = {k: max(v) for k, v in counts.items()}
        else:
            counts = {k: sum(v) / len(v) for k, v in counts.items()}
        return counts

    @classproperty
    def available_languages(cls) -> Set[str]:
        """
        Return languages supported by this detector implementation in this state.
        This should be a set of languages this detector is capable of recognizing.
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            Set[str]: A set of language codes supported by this detector.
        """
        return set()  # TODO


if __name__ == "__main__":

    weights = {
        "ovos-lang-detector-plugin-cld3": 0.8,
        "ovos-lang-detector-plugin-cld2": 0.8,
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
