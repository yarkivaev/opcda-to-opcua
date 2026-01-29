# -*- coding: utf-8 -*-
"""
Tests for TagValue domain object.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.domain.value import TagValue

logging.disable(logging.CRITICAL)


class TestTagValue(unittest.TestCase):
    """Tests for TagValue."""

    def test_tagvalue_content_returns_integer(self):
        content = random.randint(-1000, 1000)
        self.assertEqual(
            TagValue(content).content(),
            content,
            "TagValue.content should return integer"
        )

    def test_tagvalue_content_returns_float(self):
        content = random.uniform(-100.0, 100.0)
        self.assertEqual(
            TagValue(content).content(),
            content,
            "TagValue.content should return float"
        )

    def test_tagvalue_content_returns_string(self):
        content = "".join(random.choice(string.ascii_letters) for _ in range(10))
        self.assertEqual(
            TagValue(content).content(),
            content,
            "TagValue.content should return string"
        )

    def test_tagvalue_content_returns_boolean(self):
        content = random.choice([True, False])
        self.assertEqual(
            TagValue(content).content(),
            content,
            "TagValue.content should return boolean"
        )

    def test_tagvalue_content_preserves_cyrillic(self):
        content = u"\u041f\u0440\u0438\u0432\u0435\u0442"
        self.assertEqual(
            TagValue(content).content(),
            content,
            "TagValue.content should preserve Cyrillic"
        )

    def test_tagvalue_json_returns_integer(self):
        content = random.randint(1, 100)
        self.assertEqual(
            TagValue(content).json(),
            content,
            "TagValue.json should return integer"
        )

    def test_tagvalue_json_returns_float(self):
        content = random.uniform(1.0, 100.0)
        self.assertEqual(
            TagValue(content).json(),
            content,
            "TagValue.json should return float"
        )

    def test_tagvalue_equals_another_with_same_content(self):
        content = random.randint(1, 1000)
        self.assertEqual(
            TagValue(content),
            TagValue(content),
            "TagValues with same content should be equal"
        )

    def test_tagvalue_not_equals_different_content(self):
        self.assertNotEqual(
            TagValue(random.randint(1, 100)),
            TagValue(random.randint(200, 300)),
            "TagValues with different content should not be equal"
        )

    def test_tagvalue_repr_shows_content(self):
        content = random.randint(1, 100)
        self.assertIn(
            str(content),
            repr(TagValue(content)),
            "TagValue repr should show content"
        )


if __name__ == "__main__":
    unittest.main()
