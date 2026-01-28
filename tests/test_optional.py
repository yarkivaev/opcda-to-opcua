# -*- coding: utf-8 -*-
"""
Unit tests for Optional monad.

Tests follow Elegant Objects testing principles:
- One assertion per test
- Test names are full English sentences
- Random inputs where applicable
- No setUp/tearDown idioms
- No shared constants between tests
"""
import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.result.optional import Optional, Some, Empty


class SomeReportsPresentAsTrueTest(unittest.TestCase):
    """Some reports present as true."""

    def test(self):
        content = random.randint(-1000, 1000)
        result = Some(content)
        self.assertTrue(
            result.present(),
            "Some must report present as true"
        )


class SomeReturnsWrappedContentTest(unittest.TestCase):
    """Some returns wrapped content."""

    def test(self):
        content = u"\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435"
        result = Some(content)
        self.assertEqual(
            result.content(),
            content,
            "Some must return wrapped content"
        )


class SomeReturnsIntegerContentTest(unittest.TestCase):
    """Some returns integer content unchanged."""

    def test(self):
        content = random.randint(-999999, 999999)
        result = Some(content)
        self.assertEqual(
            result.content(),
            content,
            "Some must return integer content unchanged"
        )


class SomeReturnsFloatContentTest(unittest.TestCase):
    """Some returns float content unchanged."""

    def test(self):
        content = random.uniform(-1000.0, 1000.0)
        result = Some(content)
        self.assertAlmostEqual(
            result.content(),
            content,
            places=10,
            msg="Some must return float content unchanged"
        )


class SomeOtherwiseReturnsContentTest(unittest.TestCase):
    """Some otherwise returns content ignoring default."""

    def test(self):
        content = random.randint(1, 100)
        default = random.randint(101, 200)
        result = Some(content)
        self.assertEqual(
            result.otherwise(default),
            content,
            "Some otherwise must return content ignoring default"
        )


class SomeMapsContentWithFunctionTest(unittest.TestCase):
    """Some maps content with function."""

    def test(self):
        content = random.randint(1, 100)
        result = Some(content)
        doubled = result.map(lambda x: x * 2)
        self.assertEqual(
            doubled.content(),
            content * 2,
            "Some must map content with function"
        )


class SomeMapsToNewSomeInstanceTest(unittest.TestCase):
    """Some map returns new Some instance."""

    def test(self):
        original = Some(random.randint(1, 100))
        mapped = original.map(lambda x: x)
        self.assertIsNot(
            original,
            mapped,
            "Some map must return new instance"
        )


class SomeFlatmapsToNewOptionalTest(unittest.TestCase):
    """Some flatmaps to new Optional."""

    def test(self):
        result = Some(random.randint(10, 100))
        chained = result.flatmap(lambda x: Some(x + 5) if x > 5 else Empty())
        self.assertTrue(
            chained.present(),
            "Some must flatmap to new Optional"
        )


class SomeFlatmapsToEmptyOnConditionTest(unittest.TestCase):
    """Some flatmaps to Empty when condition fails."""

    def test(self):
        result = Some(random.randint(-10, 0))
        chained = result.flatmap(lambda x: Some(x) if x > 50 else Empty())
        self.assertFalse(
            chained.present(),
            "Some must flatmap to Empty when condition fails"
        )


class SomeHandlesListContentTest(unittest.TestCase):
    """Some handles list content."""

    def test(self):
        content = [random.randint(1, 100) for _ in range(5)]
        result = Some(content)
        self.assertEqual(
            result.content(),
            content,
            "Some must handle list content"
        )


class SomeHandlesDictContentTest(unittest.TestCase):
    """Some handles dict content."""

    def test(self):
        content = {"key_%d" % i: random.randint(1, 100) for i in range(3)}
        result = Some(content)
        self.assertEqual(
            result.content(),
            content,
            "Some must handle dict content"
        )


class EmptyReportsPresentAsFalseTest(unittest.TestCase):
    """Empty reports present as false."""

    def test(self):
        result = Empty()
        self.assertFalse(
            result.present(),
            "Empty must report present as false"
        )


class EmptyRaisesOnContentExtractionTest(unittest.TestCase):
    """Empty raises RuntimeError on content extraction."""

    def test(self):
        result = Empty()
        with self.assertRaises(RuntimeError):
            result.content()


class EmptyOtherwiseReturnsDefaultTest(unittest.TestCase):
    """Empty otherwise returns default."""

    def test(self):
        default = random.randint(1, 100)
        result = Empty()
        self.assertEqual(
            result.otherwise(default),
            default,
            "Empty otherwise must return default"
        )


class EmptyOtherwiseReturnsUnicodeDefaultTest(unittest.TestCase):
    """Empty otherwise returns unicode default."""

    def test(self):
        default = u"\u041f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e"
        result = Empty()
        self.assertEqual(
            result.otherwise(default),
            default,
            "Empty otherwise must return unicode default"
        )


class EmptyMapReturnsSelfTest(unittest.TestCase):
    """Empty map returns self unchanged."""

    def test(self):
        result = Empty()
        mapped = result.map(lambda x: x * 2)
        self.assertIs(
            mapped,
            result,
            "Empty map must return self unchanged"
        )


class EmptyFlatmapReturnsSelfTest(unittest.TestCase):
    """Empty flatmap returns self unchanged."""

    def test(self):
        result = Empty()
        chained = result.flatmap(lambda x: Some(x * 2))
        self.assertIs(
            chained,
            result,
            "Empty flatmap must return self unchanged"
        )


class EmptyRemainsPresentFalseAfterMapTest(unittest.TestCase):
    """Empty remains present false after map."""

    def test(self):
        result = Empty()
        mapped = result.map(lambda x: x * 2)
        self.assertFalse(
            mapped.present(),
            "Empty must remain present false after map"
        )


class EmptyOtherwiseReturnsListDefaultTest(unittest.TestCase):
    """Empty otherwise returns list default."""

    def test(self):
        default = [random.randint(1, 10) for _ in range(3)]
        result = Empty()
        self.assertEqual(
            result.otherwise(default),
            default,
            "Empty otherwise must return list default"
        )


class MultipleEmptyInstancesAreIndependentTest(unittest.TestCase):
    """Multiple Empty instances are independent."""

    def test(self):
        empty1 = Empty()
        empty2 = Empty()
        self.assertIsNot(
            empty1,
            empty2,
            "Multiple Empty instances must be independent"
        )


if __name__ == "__main__":
    unittest.main()
