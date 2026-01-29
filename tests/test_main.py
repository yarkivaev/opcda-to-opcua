# -*- coding: utf-8 -*-
"""
Tests for main module helpers.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.app.main import _matches

logging.disable(logging.CRITICAL)


class TestMatches(unittest.TestCase):
    """Tests for _matches helper function."""

    def test_matches_returns_true_for_exact_pattern(self):
        text = "COM1.Device exchange"
        patterns = ["COM1.Device exchange"]
        self.assertTrue(
            _matches(text, patterns),
            "_matches should return True for exact pattern"
        )

    def test_matches_returns_true_for_wildcard_pattern(self):
        text = "COM1.Device exchange"
        patterns = ["*.Device exchange"]
        self.assertTrue(
            _matches(text, patterns),
            "_matches should return True for wildcard pattern"
        )

    def test_matches_returns_false_for_no_match(self):
        text = "COM1.Temperature"
        patterns = ["*.Device exchange"]
        self.assertFalse(
            _matches(text, patterns),
            "_matches should return False when no pattern matches"
        )

    def test_matches_returns_false_for_empty_patterns(self):
        text = "COM1.Temperature"
        patterns = []
        self.assertFalse(
            _matches(text, patterns),
            "_matches should return False for empty patterns"
        )

    def test_matches_handles_multiple_patterns(self):
        text = "COM1.Status"
        patterns = ["*.Device exchange", "*.Status"]
        self.assertTrue(
            _matches(text, patterns),
            "_matches should return True when any pattern matches"
        )

    def test_matches_handles_random_text_with_no_match(self):
        text = "".join(random.choice(string.ascii_letters) for _ in range(15))
        patterns = ["*.Device exchange", "*.Status"]
        self.assertFalse(
            _matches(text, patterns),
            "_matches should return False for random text"
        )

    def test_matches_handles_cyrillic_text(self):
        text = u"COM1.\u0422\u041c_5104.Device exchange"
        patterns = ["*.Device exchange"]
        self.assertTrue(
            _matches(text, patterns),
            "_matches should handle Cyrillic text"
        )

    def test_matches_handles_question_mark_wildcard(self):
        text = "COM1.Tag1"
        patterns = ["COM1.Tag?"]
        self.assertTrue(
            _matches(text, patterns),
            "_matches should handle ? wildcard"
        )

    def test_matches_handles_character_class(self):
        text = "COM1.Tag1"
        patterns = ["COM1.Tag[123]"]
        self.assertTrue(
            _matches(text, patterns),
            "_matches should handle character class"
        )


if __name__ == "__main__":
    unittest.main()
