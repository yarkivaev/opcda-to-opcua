# -*- coding: utf-8 -*-
"""
Tests for DaSource and FakeDaSource.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.da.fake import FakeDaSource
from opcda_to_mqtt.domain.path import TagPath

logging.disable(logging.CRITICAL)


class TestFakeDaSource(unittest.TestCase):
    """Tests for FakeDaSource."""

    def test_fake_source_discover_returns_right(self):
        tags = [TagPath("Tag1"), TagPath("Tag2")]
        source = FakeDaSource(tags)
        result = source.discover("prefix")
        self.assertTrue(
            result.is_right(),
            "FakeDaSource.discover should return Right"
        )

    def test_fake_source_discover_returns_configured_tags(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(10))
        tags = [TagPath(path)]
        source = FakeDaSource(tags)
        result = source.discover("")
        discovered = result.fold(lambda e: [], lambda t: t)
        self.assertEqual(
            len(discovered),
            1,
            "FakeDaSource should return configured tags"
        )

    def test_fake_source_discover_ignores_prefix(self):
        tags = [TagPath("A"), TagPath("B")]
        source = FakeDaSource(tags)
        prefix = "".join(random.choice(string.ascii_letters) for _ in range(5))
        result = source.discover(prefix)
        discovered = result.fold(lambda e: [], lambda t: t)
        self.assertEqual(
            len(discovered),
            2,
            "FakeDaSource should ignore prefix"
        )

    def test_fake_source_tags_returns_copy(self):
        tags = [TagPath("Original")]
        source = FakeDaSource(tags)
        returned = source.tags()
        returned.append(TagPath("Added"))
        self.assertEqual(
            len(source.tags()),
            1,
            "FakeDaSource.tags should return a copy"
        )

    def test_fake_source_discover_returns_independent_list(self):
        tags = [TagPath("Tag")]
        source = FakeDaSource(tags)
        result1 = source.discover("")
        list1 = result1.fold(lambda e: [], lambda t: t)
        list1.append(TagPath("New"))
        result2 = source.discover("")
        list2 = result2.fold(lambda e: [], lambda t: t)
        self.assertEqual(
            len(list2),
            1,
            "Each discover call should return independent list"
        )

    def test_fake_source_handles_empty_tags(self):
        source = FakeDaSource([])
        result = source.discover("any")
        discovered = result.fold(lambda e: ["error"], lambda t: t)
        self.assertEqual(
            len(discovered),
            0,
            "FakeDaSource should handle empty tags"
        )

    def test_fake_source_preserves_cyrillic_tags(self):
        path = u"COM1.\u0422\u041c_5104"
        tags = [TagPath(path)]
        source = FakeDaSource(tags)
        result = source.discover("")
        discovered = result.fold(lambda e: [], lambda t: t)
        self.assertEqual(
            discovered[0].text(),
            path,
            "FakeDaSource should preserve Cyrillic tags"
        )


if __name__ == "__main__":
    unittest.main()
