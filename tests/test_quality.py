# -*- coding: utf-8 -*-
"""
Tests for OpcQuality domain object.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.domain.quality import OpcQuality

logging.disable(logging.CRITICAL)


class TestOpcQuality(unittest.TestCase):
    """Tests for OpcQuality."""

    def test_opcquality_text_returns_lowercase(self):
        self.assertEqual(
            OpcQuality("Good").text(),
            "good",
            "OpcQuality.text should return lowercase"
        )

    def test_opcquality_text_handles_mixed_case(self):
        self.assertEqual(
            OpcQuality("GOOD").text(),
            "good",
            "OpcQuality.text should handle uppercase"
        )

    def test_opcquality_text_handles_bad(self):
        self.assertEqual(
            OpcQuality("Bad").text(),
            "bad",
            "OpcQuality.text should handle Bad"
        )

    def test_opcquality_text_handles_uncertain(self):
        self.assertEqual(
            OpcQuality("Uncertain").text(),
            "uncertain",
            "OpcQuality.text should handle Uncertain"
        )

    def test_opcquality_is_good_returns_true_for_good(self):
        self.assertTrue(
            OpcQuality("Good").is_good(),
            "OpcQuality.is_good should return True for Good"
        )

    def test_opcquality_is_good_returns_true_for_good_with_suffix(self):
        self.assertTrue(
            OpcQuality("GoodLocalOverride").is_good(),
            "OpcQuality.is_good should return True for GoodLocalOverride"
        )

    def test_opcquality_is_good_returns_false_for_bad(self):
        self.assertFalse(
            OpcQuality("Bad").is_good(),
            "OpcQuality.is_good should return False for Bad"
        )

    def test_opcquality_is_good_returns_false_for_uncertain(self):
        self.assertFalse(
            OpcQuality("Uncertain").is_good(),
            "OpcQuality.is_good should return False for Uncertain"
        )

    def test_opcquality_equals_another_with_same_code(self):
        self.assertEqual(
            OpcQuality("Good"),
            OpcQuality("Good"),
            "OpcQualities with same code should be equal"
        )

    def test_opcquality_equals_ignores_case(self):
        self.assertEqual(
            OpcQuality("good"),
            OpcQuality("GOOD"),
            "OpcQuality equality should ignore case"
        )

    def test_opcquality_not_equals_different_code(self):
        self.assertNotEqual(
            OpcQuality("Good"),
            OpcQuality("Bad"),
            "OpcQualities with different codes should not be equal"
        )

    def test_opcquality_repr_shows_code(self):
        code = "Good"
        self.assertIn(
            code,
            repr(OpcQuality(code)),
            "OpcQuality repr should show code"
        )


if __name__ == "__main__":
    unittest.main()
