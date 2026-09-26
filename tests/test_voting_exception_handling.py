"""Tests for per-detector exception isolation in VotingLangDetectPlugin (refs ovos-persona-server#39)."""
import unittest
from unittest.mock import MagicMock, patch

from ovos_lang_detector_classics_plugin import VotingLangDetectPlugin


def _make_plugin(detect_probs_result=None, raise_exc=None):
    """Return a minimal LanguageDetector mock."""
    mock = MagicMock()
    if raise_exc is not None:
        mock.detect_probs.side_effect = raise_exc
    else:
        mock.detect_probs.return_value = detect_probs_result or {}
    return mock


class TestVotingDetectProbsExceptionIsolation(unittest.TestCase):

    def _make_voting_plugin(self, voters):
        """Build a VotingLangDetectPlugin with pre-loaded voters (bypasses load_plugins)."""
        weights = {name: 1.0 for name in voters}
        plugin = VotingLangDetectPlugin.__new__(VotingLangDetectPlugin)
        plugin.config = {"weights": weights}
        plugin.weights = weights
        plugin.voters = voters
        return plugin

    def test_one_detector_raises_others_still_contribute(self):
        """A per-detector exception must not prevent other voters from contributing."""
        bad = _make_plugin(raise_exc=AttributeError("'boost'"))  # cld2-style crash
        good = _make_plugin(detect_probs_result={"en": 0.9, "fr": 0.1})
        plugin = self._make_voting_plugin({"cld2": bad, "langdetect": good})

        result = plugin.detect_probs("hello world")

        self.assertIn("en", result)
        self.assertAlmostEqual(result["en"], 0.9)

    def test_all_detectors_raise_returns_empty(self):
        """If every voter raises, detect_probs should return an empty dict (no crash)."""
        bad1 = _make_plugin(raise_exc=AttributeError("'boost'"))
        bad2 = _make_plugin(raise_exc=RuntimeError("some other error"))
        plugin = self._make_voting_plugin({"cld2": bad1, "cld3": bad2})

        result = plugin.detect_probs("hello world")
        self.assertEqual(result, {})

    def test_good_detector_result_unchanged_when_peer_raises(self):
        """The surviving voter's probabilities must be averaged only over its own count."""
        good = _make_plugin(detect_probs_result={"pt": 0.8, "es": 0.2})
        bad = _make_plugin(raise_exc=Exception("crash"))
        plugin = self._make_voting_plugin({"good": good, "bad": bad})

        result = plugin.detect_probs("olá mundo")
        # Only one voter contributed, so no averaging divisor issue
        self.assertIn("pt", result)
        self.assertAlmostEqual(result["pt"], 0.8)

    def test_no_exception_path_unchanged(self):
        """When no voter raises, behaviour must be identical to the original implementation."""
        v1 = _make_plugin(detect_probs_result={"en": 0.6, "de": 0.4})
        v2 = _make_plugin(detect_probs_result={"en": 0.8, "de": 0.2})
        plugin = self._make_voting_plugin({"p1": v1, "p2": v2})

        result = plugin.detect_probs("hello")
        # average of [0.6, 0.8] = 0.7 for "en"; average of [0.4, 0.2] = 0.3 for "de"
        self.assertAlmostEqual(result["en"], 0.7)
        self.assertAlmostEqual(result["de"], 0.3)

    def test_detect_still_works_after_partial_failure(self):
        """detect() (which calls detect_probs) must return a language even when one voter crashes."""
        bad = _make_plugin(raise_exc=AttributeError("'boost'"))
        good = _make_plugin(detect_probs_result={"es": 0.95, "pt": 0.05})
        plugin = self._make_voting_plugin({"cld2": bad, "langdetect": good})

        lang = plugin.detect("hola mundo")
        self.assertEqual(lang, "es")


if __name__ == "__main__":
    unittest.main()
