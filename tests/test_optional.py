# -*- coding: utf-8 -*-
"""
Tests for Optional ADT.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.result.optional import Optional, Some, Empty

logging.disable(logging.CRITICAL)


class TestSome(unittest.TestCase):
    """Tests for Some present case."""

    def test_some_fold_applies_some_function_to_content(self):
        content = random.randint(1, 1000)
        result = Some(content).fold(
            lambda: "empty",
            lambda v: v * 2
        )
        self.assertEqual(
            result,
            content * 2,
            "Some.fold should apply some function"
        )

    def test_some_is_present_returns_true(self):
        content = "".join(random.choice(string.ascii_letters) for _ in range(8))
        self.assertTrue(
            Some(content).is_present(),
            "Some.is_present should return True"
        )

    def test_some_map_transforms_content(self):
        content = random.randint(1, 100)
        result = Some(content).map(lambda x: x + 10)
        self.assertEqual(
            result.fold(lambda: 0, lambda v: v),
            content + 10,
            "Some.map should transform content"
        )

    def test_some_flatmap_returns_function_result(self):
        content = random.randint(1, 50)
        result = Some(content).flatmap(lambda x: Some(x * 3))
        self.assertEqual(
            result.fold(lambda: 0, lambda v: v),
            content * 3,
            "Some.flatmap should return function result"
        )

    def test_some_otherwise_returns_content(self):
        content = random.randint(1, 100)
        default = random.randint(200, 300)
        self.assertEqual(
            Some(content).otherwise(default),
            content,
            "Some.otherwise should return content"
        )

    def test_some_content_returns_wrapped_value(self):
        content = "".join(random.choice(string.ascii_letters) for _ in range(10))
        self.assertEqual(
            Some(content).content(),
            content,
            "Some.content should return wrapped value"
        )

    def test_some_equals_another_some_with_same_content(self):
        content = random.randint(1, 1000)
        self.assertEqual(
            Some(content),
            Some(content),
            "Somes with same content should be equal"
        )

    def test_some_not_equals_some_with_different_content(self):
        self.assertNotEqual(
            Some(random.randint(1, 100)),
            Some(random.randint(200, 300)),
            "Somes with different content should not be equal"
        )

    def test_some_not_equals_empty(self):
        content = random.randint(1, 100)
        self.assertNotEqual(
            Some(content),
            Empty(),
            "Some should not equal Empty"
        )

    def test_some_repr_shows_content(self):
        content = random.randint(1, 100)
        self.assertIn(
            str(content),
            repr(Some(content)),
            "Some repr should show content"
        )


class TestEmpty(unittest.TestCase):
    """Tests for Empty absent case."""

    def test_empty_fold_applies_empty_function(self):
        marker = "".join(random.choice(string.ascii_letters) for _ in range(8))
        result = Empty().fold(
            lambda: marker,
            lambda v: "present"
        )
        self.assertEqual(
            result,
            marker,
            "Empty.fold should apply empty function"
        )

    def test_empty_is_present_returns_false(self):
        self.assertFalse(
            Empty().is_present(),
            "Empty.is_present should return False"
        )

    def test_empty_map_returns_empty(self):
        result = Empty().map(lambda x: x * 2)
        self.assertFalse(
            result.is_present(),
            "Empty.map should return Empty"
        )

    def test_empty_flatmap_returns_empty(self):
        result = Empty().flatmap(lambda x: Some(x * 2))
        self.assertFalse(
            result.is_present(),
            "Empty.flatmap should return Empty"
        )

    def test_empty_otherwise_returns_default(self):
        default = random.randint(1, 100)
        self.assertEqual(
            Empty().otherwise(default),
            default,
            "Empty.otherwise should return default"
        )

    def test_empty_equals_another_empty(self):
        self.assertEqual(
            Empty(),
            Empty(),
            "Empties should be equal"
        )

    def test_empty_repr_shows_empty(self):
        self.assertEqual(
            repr(Empty()),
            "Empty()",
            "Empty repr should show Empty()"
        )


if __name__ == "__main__":
    unittest.main()
