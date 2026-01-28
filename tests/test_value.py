# -*- coding: utf-8 -*-
"""
Unit tests for Value domain object.
"""
import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.domain.value import TagValue
from opcda_to_opcua.domain.variant import IntVariant, FloatVariant, StringVariant


class TagValueReturnsContentTest(unittest.TestCase):
    """TagValue returns content."""

    def test(self):
        content = random.randint(-1000, 1000)
        value = TagValue(content, IntVariant())
        self.assertEqual(
            value.content(),
            content,
            "TagValue must return content"
        )


class TagValueReturnsVariantTest(unittest.TestCase):
    """TagValue returns variant."""

    def test(self):
        variant = IntVariant()
        value = TagValue(42, variant)
        self.assertEqual(
            value.variant().code(),
            variant.code(),
            "TagValue must return variant"
        )


class TagValueHandlesFloatContentTest(unittest.TestCase):
    """TagValue handles float content."""

    def test(self):
        content = random.uniform(-1000.0, 1000.0)
        value = TagValue(content, FloatVariant())
        self.assertAlmostEqual(
            value.content(),
            content,
            places=10,
            msg="TagValue must handle float content"
        )


class TagValueHandlesStringContentTest(unittest.TestCase):
    """TagValue handles string content."""

    def test(self):
        content = u"\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435_%d" % random.randint(1, 100)
        value = TagValue(content, StringVariant())
        self.assertEqual(
            value.content(),
            content,
            "TagValue must handle string content"
        )


class TagValueEqualityTest(unittest.TestCase):
    """TagValue equality compares content and variant."""

    def test(self):
        content = random.randint(1, 100)
        value1 = TagValue(content, IntVariant())
        value2 = TagValue(content, IntVariant())
        self.assertEqual(
            value1,
            value2,
            "TagValues with same content and variant must be equal"
        )


class TagValueInequalityByContentTest(unittest.TestCase):
    """TagValue inequality for different content."""

    def test(self):
        value1 = TagValue(42, IntVariant())
        value2 = TagValue(43, IntVariant())
        self.assertNotEqual(
            value1,
            value2,
            "TagValues with different content must not be equal"
        )


class TagValueInequalityByVariantTest(unittest.TestCase):
    """TagValue inequality for different variant."""

    def test(self):
        value1 = TagValue(42, IntVariant())
        value2 = TagValue(42, FloatVariant())
        self.assertNotEqual(
            value1,
            value2,
            "TagValues with different variant must not be equal"
        )


class TagValueHashConsistencyTest(unittest.TestCase):
    """TagValue hash is consistent with equality."""

    def test(self):
        content = random.randint(1, 100)
        value1 = TagValue(content, IntVariant())
        value2 = TagValue(content, IntVariant())
        self.assertEqual(
            hash(value1),
            hash(value2),
            "Equal TagValues must have equal hashes"
        )


class TagValueHandlesListContentTest(unittest.TestCase):
    """TagValue handles list content."""

    def test(self):
        content = [random.randint(1, 10) for _ in range(5)]
        value = TagValue(content, IntVariant())
        self.assertEqual(
            value.content(),
            content,
            "TagValue must handle list content"
        )


class TagValueHandlesBoolContentTest(unittest.TestCase):
    """TagValue handles bool content."""

    def test(self):
        content = random.choice([True, False])
        value = TagValue(content, IntVariant())
        self.assertEqual(
            value.content(),
            content,
            "TagValue must handle bool content"
        )


if __name__ == "__main__":
    unittest.main()
