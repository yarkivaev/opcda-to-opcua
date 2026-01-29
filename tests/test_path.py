# -*- coding: utf-8 -*-
"""
Tests for TagPath domain object.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.domain.path import TagPath

logging.disable(logging.CRITICAL)


class TestTagPath(unittest.TestCase):
    """Tests for TagPath."""

    def test_tagpath_text_returns_original_path(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(12))
        self.assertEqual(
            TagPath(path).text(),
            path,
            "TagPath.text should return original path"
        )

    def test_tagpath_text_preserves_cyrillic_characters(self):
        path = u"\u0422\u041c 5104_\u0418\u0427\u04221"
        self.assertEqual(
            TagPath(path).text(),
            path,
            "TagPath.text should preserve Cyrillic characters"
        )

    def test_tagpath_topic_prepends_prefix(self):
        path = "Device.Sensor"
        prefix = "factory/line1"
        self.assertEqual(
            TagPath(path).topic(prefix),
            "factory/line1/Device.Sensor",
            "TagPath.topic should prepend prefix with slash"
        )

    def test_tagpath_topic_with_empty_prefix(self):
        path = "COM1.Tag"
        self.assertEqual(
            TagPath(path).topic(""),
            "/COM1.Tag",
            "TagPath.topic with empty prefix should start with slash"
        )

    def test_tagpath_raises_on_empty_path(self):
        with self.assertRaises(ValueError):
            TagPath("")

    def test_tagpath_equals_another_with_same_path(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(10))
        self.assertEqual(
            TagPath(path),
            TagPath(path),
            "TagPaths with same path should be equal"
        )

    def test_tagpath_not_equals_different_path(self):
        self.assertNotEqual(
            TagPath("path.one"),
            TagPath("path.two"),
            "TagPaths with different paths should not be equal"
        )

    def test_tagpath_hash_is_consistent(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(8))
        tag = TagPath(path)
        self.assertEqual(
            hash(tag),
            hash(TagPath(path)),
            "TagPath hash should be consistent"
        )

    def test_tagpath_can_be_used_in_set(self):
        path = "COM1.Device.Tag"
        tags = {TagPath(path), TagPath(path)}
        self.assertEqual(
            len(tags),
            1,
            "Duplicate TagPaths should be deduplicated in set"
        )

    def test_tagpath_can_be_used_as_dict_key(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(10))
        mapping = {TagPath(path): 42}
        self.assertEqual(
            mapping[TagPath(path)],
            42,
            "TagPath should work as dict key"
        )

    def test_tagpath_repr_shows_path(self):
        path = "Device.Sensor.Temp"
        self.assertIn(
            path,
            repr(TagPath(path)),
            "TagPath repr should show path"
        )


if __name__ == "__main__":
    unittest.main()
