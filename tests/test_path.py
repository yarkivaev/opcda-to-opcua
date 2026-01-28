# -*- coding: utf-8 -*-
"""
Unit tests for Path domain object.
"""
import unittest
import random
import string
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.domain.path import NodePath, ParsedPath


class NodePathReturnsSegmentsListTest(unittest.TestCase):
    """NodePath returns segments as list."""

    def test(self):
        segments = ["Seg%d" % random.randint(1, 100) for _ in range(3)]
        path = NodePath(segments)
        self.assertEqual(
            path.segments(),
            segments,
            "NodePath must return segments as list"
        )


class NodePathFormatsTextWithSeparatorTest(unittest.TestCase):
    """NodePath formats text with separator."""

    def test(self):
        segments = ["Objects", "Device", "Temperature"]
        path = NodePath(segments, ".")
        self.assertEqual(
            path.text(),
            "Objects.Device.Temperature",
            "NodePath must format text with separator"
        )


class NodePathFormatsTextWithCustomSeparatorTest(unittest.TestCase):
    """NodePath formats text with custom separator."""

    def test(self):
        segments = ["A", "B", "C"]
        path = NodePath(segments, "/")
        self.assertEqual(
            path.text(),
            "A/B/C",
            "NodePath must format text with custom separator"
        )


class NodePathExtractsNameAsLastSegmentTest(unittest.TestCase):
    """NodePath extracts name as last segment."""

    def test(self):
        name = "Tag%d" % random.randint(1, 1000)
        segments = ["Parent", name]
        path = NodePath(segments)
        self.assertEqual(
            path.name(),
            name,
            "NodePath must extract name as last segment"
        )


class NodePathReturnsEmptyNameForEmptySegmentsTest(unittest.TestCase):
    """NodePath returns empty name for empty segments."""

    def test(self):
        path = NodePath([])
        self.assertEqual(
            path.name(),
            "",
            "NodePath must return empty name for empty segments"
        )


class NodePathSegmentsAreImmutableTest(unittest.TestCase):
    """NodePath segments are immutable."""

    def test(self):
        segments = ["A", "B", "C"]
        path = NodePath(segments)
        returned = path.segments()
        returned.append("D")
        self.assertEqual(
            len(path.segments()),
            3,
            "NodePath segments must be immutable"
        )


class NodePathHandlesUnicodeSegmentsTest(unittest.TestCase):
    """NodePath handles unicode segments."""

    def test(self):
        segments = [u"\u041e\u0431\u044a\u0435\u043a\u0442\u044b", u"\u0422\u0435\u043c\u043f"]
        path = NodePath(segments)
        self.assertEqual(
            path.segments(),
            segments,
            "NodePath must handle unicode segments"
        )


class NodePathParentReturnsSomeForNestedPathTest(unittest.TestCase):
    """NodePath parent returns Some for nested path."""

    def test(self):
        path = NodePath(["A", "B", "C"])
        parent = path.parent()
        self.assertTrue(
            parent.present(),
            "NodePath parent must return Some for nested path"
        )


class NodePathParentReturnsCorrectPathTest(unittest.TestCase):
    """NodePath parent returns correct path."""

    def test(self):
        path = NodePath(["A", "B", "C"])
        parent = path.parent()
        self.assertEqual(
            parent.content().segments(),
            ["A", "B"],
            "NodePath parent must return correct path"
        )


class NodePathParentReturnsEmptyForSingleSegmentTest(unittest.TestCase):
    """NodePath parent returns Empty for single segment."""

    def test(self):
        path = NodePath(["Root"])
        parent = path.parent()
        self.assertFalse(
            parent.present(),
            "NodePath parent must return Empty for single segment"
        )


class NodePathParentReturnsEmptyForEmptyPathTest(unittest.TestCase):
    """NodePath parent returns Empty for empty path."""

    def test(self):
        path = NodePath([])
        parent = path.parent()
        self.assertFalse(
            parent.present(),
            "NodePath parent must return Empty for empty path"
        )


class NodePathEqualityTest(unittest.TestCase):
    """NodePath equality compares segments."""

    def test(self):
        segments = ["A", "B", "C"]
        path1 = NodePath(segments)
        path2 = NodePath(segments)
        self.assertEqual(
            path1,
            path2,
            "NodePaths with same segments must be equal"
        )


class NodePathInequalityTest(unittest.TestCase):
    """NodePath inequality for different segments."""

    def test(self):
        path1 = NodePath(["A", "B"])
        path2 = NodePath(["A", "C"])
        self.assertNotEqual(
            path1,
            path2,
            "NodePaths with different segments must not be equal"
        )


class NodePathHashConsistencyTest(unittest.TestCase):
    """NodePath hash is consistent with equality."""

    def test(self):
        segments = ["X", "Y", "Z"]
        path1 = NodePath(segments)
        path2 = NodePath(segments)
        self.assertEqual(
            hash(path1),
            hash(path2),
            "Equal NodePaths must have equal hashes"
        )


class ParsedPathParsesTextTest(unittest.TestCase):
    """ParsedPath parses text into NodePath."""

    def test(self):
        text = "Simulation.Random.Int%d" % random.randint(1, 100)
        parsed = ParsedPath(text)
        path = parsed.path()
        self.assertEqual(
            path.text(),
            text,
            "ParsedPath must parse text into NodePath"
        )


class ParsedPathParsesWithCustomSeparatorTest(unittest.TestCase):
    """ParsedPath parses with custom separator."""

    def test(self):
        parsed = ParsedPath("A/B/C", "/")
        path = parsed.path()
        self.assertEqual(
            path.segments(),
            ["A", "B", "C"],
            "ParsedPath must parse with custom separator"
        )


class ParsedPathHandlesUnicodeTextTest(unittest.TestCase):
    """ParsedPath handles unicode text."""

    def test(self):
        text = u"\u041e\u0431\u044a\u0435\u043a\u0442.\u0422\u0435\u0433"
        parsed = ParsedPath(text)
        path = parsed.path()
        self.assertEqual(
            path.text(),
            text,
            "ParsedPath must handle unicode text"
        )


if __name__ == "__main__":
    unittest.main()
