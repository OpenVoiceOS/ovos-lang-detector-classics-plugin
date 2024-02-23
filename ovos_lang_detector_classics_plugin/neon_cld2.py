# taken from https://github.com/NeonGeckoCom/neon-lang-plugin-cld2
from ovos_plugin_manager.templates.language import LanguageDetector
import pycld2


class Pycld2Detector(LanguageDetector):
    def cl2_detect(self, text, return_multiple=False, return_dict=False,
                   hint_language=None, filter_unreliable=False):
        """
        :param text:
        :param return_multiple bool if True return a list of all languages detected, else the top language
        :param return_dict: bool  if True returns all data, E.g.,  pt -> {'lang': 'Portuguese', 'lang_code': 'pt', 'conf': 0.96}
        :param hint_language: str  E.g., 'ITALIAN' or 'it' boosts Italian
        :return:
        """
        isReliable, textBytesFound, details = pycld2.detect(
            text, hintLanguage=hint_language)
        languages = []

        # filter unreliable predictions
        if not isReliable and filter_unreliable:
            return None

        # select first language only
        if not return_multiple:
            details = [details[0]]

        for name, code, score, _ in details:
            if code == "un":
                continue
            if return_dict:
                languages.append({"lang": name.lower().capitalize(),
                                  "lang_code": code, "conf": score / 100})
            else:
                languages.append(code)

        # return top language only
        if not return_multiple:
            if not len(languages):
                return None
            return languages[0]
        return languages

    def detect(self, text):
        if self.boost:
            return self.cl2_detect(text, hint_language=self.hint_language) or \
                   self.default_language
        else:
            return self.cl2_detect(text) or self.default_language

    def detect_probs(self, text):
        if self.boost:
            data = self.cl2_detect(text, return_multiple=True,
                                   return_dict=True,
                                   hint_language=self.hint_language)
        else:
            data = self.cl2_detect(text, return_multiple=True,
                                   return_dict=True)
        langs = {}
        for lang in data:
            langs[lang["lang_code"]] = lang["conf"]
        return langs