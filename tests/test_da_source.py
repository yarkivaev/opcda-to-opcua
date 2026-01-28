# -*- coding: utf-8 -*-
"""
Unit tests for FakeDaSource.
"""
import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.da.fake import FakeDaSource
from opcda_to_opcua.domain.path import NodePath
from opcda_to_opcua.domain.value import TagValue
from opcda_to_opcua.domain.variant import IntVariant, FloatVariant


class FakeDaSourceConnectsSuccessfullyTest(unittest.TestCase):
    """FakeDaSource connects successfully."""

    def test(self):
        source = FakeDaSource([], {})
        result = source.connect()
        self.assertTrue(
            result.successful(),
            "FakeDaSource must connect successfully"
        )


class FakeDaSourceDisconnectsSuccessfullyTest(unittest.TestCase):
    """FakeDaSource disconnects successfully."""

    def test(self):
        source = FakeDaSource([], {})
        source.connect()
        result = source.disconnect()
        self.assertTrue(
            result.successful(),
            "FakeDaSource must disconnect successfully"
        )


class FakeDaSourceFailsDiscoverWhenNotConnectedTest(unittest.TestCase):
    """FakeDaSource fails discover when not connected."""

    def test(self):
        source = FakeDaSource([], {})
        result = source.discover()
        self.assertFalse(
            result.successful(),
            "FakeDaSource must fail discover when not connected"
        )


class FakeDaSourceDiscoversNodesTest(unittest.TestCase):
    """FakeDaSource discovers nodes."""

    def test(self):
        paths = [
            NodePath(["Sim", "Int%d" % random.randint(1, 100)]),
            NodePath(["Sim", "Real%d" % random.randint(1, 100)])
        ]
        source = FakeDaSource(paths, {})
        source.connect()
        result = source.discover()
        self.assertEqual(
            len(result.value()),
            2,
            "FakeDaSource must discover all nodes"
        )


class FakeDaSourceFetchesValueTest(unittest.TestCase):
    """FakeDaSource fetches value."""

    def test(self):
        path = NodePath(["Sim", "Tag%d" % random.randint(1, 100)])
        content = random.randint(-1000, 1000)
        values = {path.text(): TagValue(content, IntVariant())}
        source = FakeDaSource([path], values)
        source.connect()
        result = source.fetch(path)
        self.assertEqual(
            result.value().value().content(),
            content,
            "FakeDaSource must fetch value"
        )


class FakeDaSourceFetchReturnsGoodQualityTest(unittest.TestCase):
    """FakeDaSource fetch returns good quality."""

    def test(self):
        path = NodePath(["Sim", "Tag"])
        values = {path.text(): TagValue(42, IntVariant())}
        source = FakeDaSource([path], values)
        source.connect()
        result = source.fetch(path)
        self.assertTrue(
            result.value().quality().good(),
            "FakeDaSource fetch must return good quality"
        )


class FakeDaSourceFailsFetchWhenNotConnectedTest(unittest.TestCase):
    """FakeDaSource fails fetch when not connected."""

    def test(self):
        path = NodePath(["Sim", "Tag"])
        values = {path.text(): TagValue(42, IntVariant())}
        source = FakeDaSource([path], values)
        result = source.fetch(path)
        self.assertFalse(
            result.successful(),
            "FakeDaSource must fail fetch when not connected"
        )


class FakeDaSourceFailsFetchForUnknownPathTest(unittest.TestCase):
    """FakeDaSource fails fetch for unknown path."""

    def test(self):
        path = NodePath(["Unknown", "Tag"])
        source = FakeDaSource([], {})
        source.connect()
        result = source.fetch(path)
        self.assertFalse(
            result.successful(),
            "FakeDaSource must fail fetch for unknown path"
        )


class FakeDaSourceSendsValueTest(unittest.TestCase):
    """FakeDaSource sends value."""

    def test(self):
        path = NodePath(["Sim", "Setpoint"])
        value = TagValue(random.randint(1, 100), IntVariant())
        source = FakeDaSource([path], {path.text(): TagValue(0, IntVariant())})
        source.connect()
        result = source.send(path, value)
        self.assertTrue(
            result.successful(),
            "FakeDaSource must send value successfully"
        )


class FakeDaSourceRecordsWrittenValueTest(unittest.TestCase):
    """FakeDaSource records written value."""

    def test(self):
        path = NodePath(["Sim", "Setpoint"])
        content = random.randint(1, 100)
        value = TagValue(content, IntVariant())
        source = FakeDaSource([path], {path.text(): TagValue(0, IntVariant())})
        source.connect()
        source.send(path, value)
        written = source.written(path)
        self.assertEqual(
            written.content().content(),
            content,
            "FakeDaSource must record written value"
        )


class FakeDaSourceWrittenReturnsEmptyForUnwrittenTest(unittest.TestCase):
    """FakeDaSource written returns Empty for unwritten path."""

    def test(self):
        path = NodePath(["Sim", "Unwritten"])
        source = FakeDaSource([], {})
        source.connect()
        written = source.written(path)
        self.assertFalse(
            written.present(),
            "FakeDaSource written must return Empty for unwritten path"
        )


class FakeDaSourceFailsSendWhenNotConnectedTest(unittest.TestCase):
    """FakeDaSource fails send when not connected."""

    def test(self):
        path = NodePath(["Sim", "Setpoint"])
        value = TagValue(42, IntVariant())
        source = FakeDaSource([path], {})
        result = source.send(path, value)
        self.assertFalse(
            result.successful(),
            "FakeDaSource must fail send when not connected"
        )


class FakeDaSourceUpdatesValueAfterWriteTest(unittest.TestCase):
    """FakeDaSource updates value after write."""

    def test(self):
        path = NodePath(["Sim", "Tag"])
        original = TagValue(0, IntVariant())
        updated = TagValue(random.randint(1, 100), IntVariant())
        source = FakeDaSource([path], {path.text(): original})
        source.connect()
        source.send(path, updated)
        result = source.fetch(path)
        self.assertEqual(
            result.value().value().content(),
            updated.content(),
            "FakeDaSource must update value after write"
        )


class FakeDaSourceInjectsValueTest(unittest.TestCase):
    """FakeDaSource injects value."""

    def test(self):
        path = NodePath(["Sim", "Tag"])
        content = random.randint(1, 100)
        source = FakeDaSource([path], {})
        source.connect()
        source.inject(path, TagValue(content, IntVariant()))
        result = source.fetch(path)
        self.assertEqual(
            result.value().value().content(),
            content,
            "FakeDaSource must inject value"
        )


if __name__ == "__main__":
    unittest.main()
