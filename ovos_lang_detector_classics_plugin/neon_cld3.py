# taken from https://github.com/NeonGeckoCom/neon-lang-plugin-cld3
from ovos_plugin_manager.templates.language import LanguageDetector
import cld3


def langcode2name(lang_code):
    LANGUAGES = (('ABKHAZIAN', 'ab'),
                 ('AFAR', 'aa'),
                 ('AFRIKAANS', 'af'),
                 ('AKAN', 'ak'),
                 ('ALBANIAN', 'sq'),
                 ('AMHARIC', 'am'),
                 ('ARABIC', 'ar'),
                 ('ARMENIAN', 'hy'),
                 ('ASSAMESE', 'as'),
                 ('AYMARA', 'ay'),
                 ('AZERBAIJANI', 'az'),
                 ('BASHKIR', 'ba'),
                 ('BASQUE', 'eu'),
                 ('BELARUSIAN', 'be'),
                 ('BENGALI', 'bn'),
                 ('BIHARI', 'bh'),
                 ('BISLAMA', 'bi'),
                 ('BOSNIAN', 'bs'),
                 ('BRETON', 'br'),
                 ('BULGARIAN', 'bg'),
                 ('BURMESE', 'my'),
                 ('CATALAN', 'ca'),
                 ('CEBUANO', 'ceb'),
                 ('CHEROKEE', 'chr'),
                 ('NYANJA', 'ny'),
                 ('CORSICAN', 'co'),
                 ('CROATIAN', 'hr'),
                 ('CROATIAN', 'hr'),
                 ('CZECH', 'cs'),
                 ('Chinese', 'zh'),
                 ('Chinese', 'zh'),
                 ('Chinese', 'zh'),
                 ('Chinese', 'zh'),
                 ('ChineseT', 'zh-Hant'),
                 ('ChineseT', 'zh-Hant'),
                 ('ChineseT', 'zh-Hant'),
                 ('ChineseT', 'zh-Hant'),
                 ('ChineseT', 'zh-Hant'),
                 ('ChineseT', 'zh-Hant'),
                 ('DANISH', 'da'),
                 ('DHIVEHI', 'dv'),
                 ('DUTCH', 'nl'),
                 ('DZONGKHA', 'dz'),
                 ('ENGLISH', 'en'),
                 ('ESPERANTO', 'eo'),
                 ('ESTONIAN', 'et'),
                 ('EWE', 'ee'),
                 ('FAROESE', 'fo'),
                 ('FIJIAN', 'fj'),
                 ('FINNISH', 'fi'),
                 ('FRENCH', 'fr'),
                 ('FRISIAN', 'fy'),
                 ('GA', 'gaa'),
                 ('GALICIAN', 'gl'),
                 ('GANDA', 'lg'),
                 ('GEORGIAN', 'ka'),
                 ('GERMAN', 'de'),
                 ('GREEK', 'el'),
                 ('GREENLANDIC', 'kl'),
                 ('GUARANI', 'gn'),
                 ('GUJARATI', 'gu'),
                 ('HAITIAN_CREOLE', 'ht'),
                 ('HAUSA', 'ha'),
                 ('HAWAIIAN', 'haw'),
                 ('HEBREW', 'iw'),
                 ('HEBREW', 'iw'),
                 ('HINDI', 'hi'),
                 ('HMONG', 'hmn'),
                 ('HUNGARIAN', 'hu'),
                 ('ICELANDIC', 'is'),
                 ('IGBO', 'ig'),
                 ('INDONESIAN', 'id'),
                 ('INTERLINGUA', 'ia'),
                 ('INTERLINGUE', 'ie'),
                 ('INUKTITUT', 'iu'),
                 ('INUPIAK', 'ik'),
                 ('IRISH', 'ga'),
                 ('ITALIAN', 'it'),
                 ('Ignore', 'xxx'),
                 ('JAVANESE', 'jw'),
                 ('JAVANESE', 'jw'),
                 ('Japanese', 'ja'),
                 ('KANNADA', 'kn'),
                 ('KASHMIRI', 'ks'),
                 ('KAZAKH', 'kk'),
                 ('KHASI', 'kha'),
                 ('KHMER', 'km'),
                 ('KINYARWANDA', 'rw'),
                 ('KRIO', 'kri'),
                 ('KURDISH', 'ku'),
                 ('KYRGYZ', 'ky'),
                 ('Korean', 'ko'),
                 ('LAOTHIAN', 'lo'),
                 ('LATIN', 'la'),
                 ('LATVIAN', 'lv'),
                 ('LIMBU', 'lif'),
                 ('LIMBU', 'lif'),
                 ('LIMBU', 'lif'),
                 ('LINGALA', 'ln'),
                 ('LITHUANIAN', 'lt'),
                 ('LOZI', 'loz'),
                 ('LUBA_LULUA', 'lua'),
                 ('LUO_KENYA_AND_TANZANIA', 'luo'),
                 ('LUXEMBOURGISH', 'lb'),
                 ('MACEDONIAN', 'mk'),
                 ('MALAGASY', 'mg'),
                 ('MALAY', 'ms'),
                 ('MALAYALAM', 'ml'),
                 ('MALTESE', 'mt'),
                 ('MANX', 'gv'),
                 ('MAORI', 'mi'),
                 ('MARATHI', 'mr'),
                 ('MAURITIAN_CREOLE', 'mfe'),
                 ('ROMANIAN', 'ro'),
                 ('MONGOLIAN', 'mn'),
                 ('MONTENEGRIN', 'sr-ME'),
                 ('MONTENEGRIN', 'sr-ME'),
                 ('MONTENEGRIN', 'sr-ME'),
                 ('MONTENEGRIN', 'sr-ME'),
                 ('NAURU', 'na'),
                 ('NDEBELE', 'nr'),
                 ('NEPALI', 'ne'),
                 ('NEWARI', 'new'),
                 ('NORWEGIAN', 'no'),
                 ('NORWEGIAN', 'no'),
                 ('NORWEGIAN_N', 'nn'),
                 ('NYANJA', 'ny'),
                 ('OCCITAN', 'oc'),
                 ('ORIYA', 'or'),
                 ('OROMO', 'om'),
                 ('OSSETIAN', 'os'),
                 ('PAMPANGA', 'pam'),
                 ('PASHTO', 'ps'),
                 ('PEDI', 'nso'),
                 ('PERSIAN', 'fa'),
                 ('POLISH', 'pl'),
                 ('PORTUGUESE', 'pt'),
                 ('PUNJABI', 'pa'),
                 ('QUECHUA', 'qu'),
                 ('RAJASTHANI', 'raj'),
                 ('RHAETO_ROMANCE', 'rm'),
                 ('ROMANIAN', 'ro'),
                 ('RUNDI', 'rn'),
                 ('RUSSIAN', 'ru'),
                 ('SAMOAN', 'sm'),
                 ('SANGO', 'sg'),
                 ('SANSKRIT', 'sa'),
                 ('SCOTS', 'sco'),
                 ('SCOTS_GAELIC', 'gd'),
                 ('SERBIAN', 'sr'),
                 ('SERBIAN', 'sr'),
                 ('SESELWA', 'crs'),
                 ('SESELWA', 'crs'),
                 ('SESOTHO', 'st'),
                 ('SHONA', 'sn'),
                 ('SINDHI', 'sd'),
                 ('SINHALESE', 'si'),
                 ('SISWANT', 'ss'),
                 ('SLOVAK', 'sk'),
                 ('SLOVENIAN', 'sl'),
                 ('SOMALI', 'so'),
                 ('SPANISH', 'es'),
                 ('SUNDANESE', 'su'),
                 ('SWAHILI', 'sw'),
                 ('SWEDISH', 'sv'),
                 ('SYRIAC', 'syr'),
                 ('TAGALOG', 'tl'),
                 ('TAJIK', 'tg'),
                 ('TAMIL', 'ta'),
                 ('TATAR', 'tt'),
                 ('TELUGU', 'te'),
                 ('THAI', 'th'),
                 ('TIBETAN', 'bo'),
                 ('TIGRINYA', 'ti'),
                 ('TONGA', 'to'),
                 ('TSONGA', 'ts'),
                 ('TSWANA', 'tn'),
                 ('TUMBUKA', 'tum'),
                 ('TURKISH', 'tr'),
                 ('TURKMEN', 'tk'),
                 ('TWI', 'tw'),
                 ('UIGHUR', 'ug'),
                 ('UKRAINIAN', 'uk'),
                 ('URDU', 'ur'),
                 ('UZBEK', 'uz'),
                 ('VENDA', 've'),
                 ('VIETNAMESE', 'vi'),
                 ('VOLAPUK', 'vo'),
                 ('WARAY_PHILIPPINES', 'war'),
                 ('WELSH', 'cy'),
                 ('WOLOF', 'wo'),
                 ('XHOSA', 'xh'),
                 ('X_Arabic', 'xx-Arab'),
                 ('X_Armenian', 'xx-Armn'),
                 ('X_Avestan', 'xx-Avst'),
                 ('X_BORK_BORK_BORK', 'zzb'),
                 ('X_Balinese', 'xx-Bali'),
                 ('X_Bamum', 'xx-Bamu'),
                 ('X_Batak', 'xx-Batk'),
                 ('X_Bengali', 'xx-Beng'),
                 ('X_Bopomofo', 'xx-Bopo'),
                 ('X_Brahmi', 'xx-Brah'),
                 ('X_Braille', 'xx-Brai'),
                 ('X_Buginese', 'xx-Bugi'),
                 ('X_Buhid', 'xx-Buhd'),
                 ('X_Canadian_Aboriginal', 'xx-Cans'),
                 ('X_Carian', 'xx-Cari'),
                 ('X_Chakma', 'xx-Cakm'),
                 ('X_Cham', 'xx-Cham'),
                 ('X_Cherokee', 'xx-Cher'),
                 ('X_Common', 'xx-Zyyy'),
                 ('X_Coptic', 'xx-Copt'),
                 ('X_Cuneiform', 'xx-Xsux'),
                 ('X_Cypriot', 'xx-Cprt'),
                 ('X_Cyrillic', 'xx-Cyrl'),
                 ('X_Deseret', 'xx-Dsrt'),
                 ('X_Devanagari', 'xx-Deva'),
                 ('X_ELMER_FUDD', 'zze'),
                 ('X_Egyptian_Hieroglyphs', 'xx-Egyp'),
                 ('X_Ethiopic', 'xx-Ethi'),
                 ('X_Georgian', 'xx-Geor'),
                 ('X_Glagolitic', 'xx-Glag'),
                 ('X_Gothic', 'xx-Goth'),
                 ('X_Greek', 'xx-Grek'),
                 ('X_Gujarati', 'xx-Gujr'),
                 ('X_Gurmukhi', 'xx-Guru'),
                 ('X_HACKER', 'zzh'),
                 ('X_Han', 'xx-Hani'),
                 ('X_Hangul', 'xx-Hang'),
                 ('X_Hanunoo', 'xx-Hano'),
                 ('X_Hebrew', 'xx-Hebr'),
                 ('X_Hiragana', 'xx-Hira'),
                 ('X_Imperial_Aramaic', 'xx-Armi'),
                 ('X_Inherited', 'xx-Qaai'),
                 ('X_Inscriptional_Pahlavi', 'xx-Phli'),
                 ('X_Inscriptional_Parthian', 'xx-Prti'),
                 ('X_Javanese', 'xx-Java'),
                 ('X_KLINGON', 'tlh'),
                 ('X_Kaithi', 'xx-Kthi'),
                 ('X_Kannada', 'xx-Knda'),
                 ('X_Katakana', 'xx-Kana'),
                 ('X_Kayah_Li', 'xx-Kali'),
                 ('X_Kharoshthi', 'xx-Khar'),
                 ('X_Khmer', 'xx-Khmr'),
                 ('X_Lao', 'xx-Laoo'),
                 ('X_Latin', 'xx-Latn'),
                 ('X_Lepcha', 'xx-Lepc'),
                 ('X_Limbu', 'xx-Limb'),
                 ('X_Linear_B', 'xx-Linb'),
                 ('X_Lisu', 'xx-Lisu'),
                 ('X_Lycian', 'xx-Lyci'),
                 ('X_Lydian', 'xx-Lydi'),
                 ('X_Malayalam', 'xx-Mlym'),
                 ('X_Mandaic', 'xx-Mand'),
                 ('X_Meetei_Mayek', 'xx-Mtei'),
                 ('X_Meroitic_Cursive', 'xx-Merc'),
                 ('X_Meroitic_Hieroglyphs', 'xx-Mero'),
                 ('X_Miao', 'xx-Plrd'),
                 ('X_Mongolian', 'xx-Mong'),
                 ('X_Myanmar', 'xx-Mymr'),
                 ('X_New_Tai_Lue', 'xx-Talu'),
                 ('X_Nko', 'xx-Nkoo'),
                 ('X_Ogham', 'xx-Ogam'),
                 ('X_Ol_Chiki', 'xx-Olck'),
                 ('X_Old_Italic', 'xx-Ital'),
                 ('X_Old_Persian', 'xx-Xpeo'),
                 ('X_Old_South_Arabian', 'xx-Sarb'),
                 ('X_Old_Turkic', 'xx-Orkh'),
                 ('X_Oriya', 'xx-Orya'),
                 ('X_Osmanya', 'xx-Osma'),
                 ('X_PIG_LATIN', 'zzp'),
                 ('X_Phags_Pa', 'xx-Phag'),
                 ('X_Phoenician', 'xx-Phnx'),
                 ('X_Rejang', 'xx-Rjng'),
                 ('X_Runic', 'xx-Runr'),
                 ('X_Samaritan', 'xx-Samr'),
                 ('X_Saurashtra', 'xx-Saur'),
                 ('X_Sharada', 'xx-Shrd'),
                 ('X_Shavian', 'xx-Shaw'),
                 ('X_Sinhala', 'xx-Sinh'),
                 ('X_Sora_Sompeng', 'xx-Sora'),
                 ('X_Sundanese', 'xx-Sund'),
                 ('X_Syloti_Nagri', 'xx-Sylo'),
                 ('X_Syriac', 'xx-Syrc'),
                 ('X_Tagalog', 'xx-Tglg'),
                 ('X_Tagbanwa', 'xx-Tagb'),
                 ('X_Tai_Le', 'xx-Tale'),
                 ('X_Tai_Tham', 'xx-Lana'),
                 ('X_Tai_Viet', 'xx-Tavt'),
                 ('X_Takri', 'xx-Takr'),
                 ('X_Tamil', 'xx-Taml'),
                 ('X_Telugu', 'xx-Telu'),
                 ('X_Thaana', 'xx-Thaa'),
                 ('X_Thai', 'xx-Thai'),
                 ('X_Tibetan', 'xx-Tibt'),
                 ('X_Tifinagh', 'xx-Tfng'),
                 ('X_Ugaritic', 'xx-Ugar'),
                 ('X_Vai', 'xx-Vaii'),
                 ('X_Yi', 'xx-Yiii'),
                 ('YIDDISH', 'yi'),
                 ('YORUBA', 'yo'),
                 ('ZHUANG', 'za'),
                 ('ZULU', 'zu'))
    lang_code = lang_code.lower()
    for name, code in LANGUAGES:
        if code == lang_code:
            return name.lower().capitalize()
    lang_code = lang_code.split("-")[0]
    for name, code in LANGUAGES:
        if code == lang_code:
            return name.lower().capitalize()
    return "Unknown"


class Pycld3Detector(LanguageDetector):
    def cld3_detect(self, text, return_multiple=False, return_dict=False,
                    hint_language=None, filter_unreliable=False):
        languages = []
        if return_multiple or hint_language:
            preds = sorted(cld3.get_frequent_languages(text, num_langs=5),
                           key=lambda i: i.probability, reverse=True)
            for pred in preds:
                if filter_unreliable and not pred.is_reliable:
                    continue
                if return_dict:
                    languages += [{"lang_code": pred.language,
                                   "lang": langcode2name(pred.language),
                                   "conf": pred.probability}]
                else:
                    languages.append(pred.language)

                if hint_language and hint_language == pred.language:
                    languages = [languages[-1]]
                    break
        else:
            pred = cld3.get_language(text)
            if filter_unreliable and not pred.is_reliable:
                pass
            elif return_dict:
                languages = [{"lang_code": pred.language,
                              "lang": langcode2name(pred.language),
                              "conf": pred.probability}]
            else:
                languages = [pred.language]

        # return top language only
        if not return_multiple:
            if not len(languages):
                return None
            return languages[0]
        return languages

    def detect(self, text):
        if self.boost:
            return self.cld3_detect(text, hint_language=self.hint_language) or \
                   self.default_language
        else:
            return self.cld3_detect(text) or self.default_language

    def detect_probs(self, text):
        if self.boost:
            data = self.cld3_detect(text, return_multiple=True,
                                    return_dict=True,
                                    hint_language=self.hint_language)
        else:
            data = self.cld3_detect(text, return_multiple=True,
                                    return_dict=True)
        langs = {}
        for lang in data:
            langs[lang["lang_code"]] = lang["conf"]
        return langs
