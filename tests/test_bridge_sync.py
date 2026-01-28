# -*- coding: utf-8 -*-
"""
Unit tests for BridgeSync.
"""
import unittest
import random
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.sync.bridge import BridgeSync
from opcda_to_opcua.da.fake import FakeDaSource
from opcda_to_opcua.ua.fake import FakeUaTarget
from opcda_to_opcua.domain.path import NodePath
from opcda_to_opcua.domain.value import TagValue
from opcda_to_opcua.domain.variant import IntVariant
from opcda_to_opcua.domain.interval import Milliseconds


class BridgeSyncStartsSuccessfullyTest(unittest.TestCase):
    """BridgeSync starts successfully."""

    def test(self):
        path = NodePath(["Sim", "Tag%d" % random.randint(1, 100)])
        values = {path.text(): TagValue(random.randint(1, 100), IntVariant())}
        source = FakeDaSource([path], values)
        target = FakeUaTarget()
        bridge = BridgeSync(source, target, Milliseconds(100))
        result = bridge.start()
        bridge.stop()
        self.assertTrue(
            result.successful(),
            "BridgeSync must start successfully"
        )


class BridgeSyncStopsSuccessfullyTest(unittest.TestCase):
    """BridgeSync stops successfully."""

    def test(self):
        path = NodePath(["Sim", "Tag"])
        values = {path.text(): TagValue(42, IntVariant())}
        source = FakeDaSource([path], values)
        target = FakeUaTarget()
        bridge = BridgeSync(source, target, Milliseconds(100))
        bridge.start()
        result = bridge.stop()
        self.assertTrue(
            result.successful(),
            "BridgeSync must stop successfully"
        )


class BridgeSyncMirrorsNodesTest(unittest.TestCase):
    """BridgeSync mirrors nodes to target."""

    def test(self):
        paths = [
            NodePath(["Sim", "Tag%d" % i])
            for i in range(random.randint(2, 5))
        ]
        values = {p.text(): TagValue(i, IntVariant()) for i, p in enumerate(paths)}
        source = FakeDaSource(paths, values)
        target = FakeUaTarget()
        bridge = BridgeSync(source, target, Milliseconds(100))
        bridge.start()
        bridge.stop()
        self.assertEqual(
            len(target.mirrored()),
            len(paths),
            "BridgeSync must mirror all nodes"
        )


class BridgeSyncPollsValuesTest(unittest.TestCase):
    """BridgeSync polls values at interval."""

    def test(self):
        path = NodePath(["Sim", "Counter"])
        content = random.randint(1, 100)
        values = {path.text(): TagValue(content, IntVariant())}
        source = FakeDaSource([path], values)
        target = FakeUaTarget()
        bridge = BridgeSync(source, target, Milliseconds(50))
        bridge.start()
        time.sleep(0.15)
        bridge.stop()
        reading = target.reading(path)
        self.assertEqual(
            reading.content().value().content(),
            content,
            "BridgeSync must poll and update values"
        )


class BridgeSyncWritesBackChangesTest(unittest.TestCase):
    """BridgeSync writes back changes from UA to DA."""

    def test(self):
        path = NodePath(["Sim", "Setpoint"])
        original = TagValue(0, IntVariant())
        values = {path.text(): original}
        source = FakeDaSource([path], values, writable={path.text()})
        target = FakeUaTarget()
        bridge = BridgeSync(source, target, Milliseconds(100))
        bridge.start()
        time.sleep(0.05)
        newcontent = random.randint(1, 100)
        target.simulate(path, TagValue(newcontent, IntVariant()))
        time.sleep(0.05)
        bridge.stop()
        written = source.written(path)
        self.assertEqual(
            written.content().content(),
            newcontent,
            "BridgeSync must write back changes"
        )


class BridgeSyncReadonlyModeDisablesWritebackTest(unittest.TestCase):
    """BridgeSync readonly mode disables writeback."""

    def test(self):
        path = NodePath(["Sim", "Setpoint"])
        values = {path.text(): TagValue(0, IntVariant())}
        source = FakeDaSource([path], values)
        target = FakeUaTarget()
        bridge = BridgeSync(source, target, Milliseconds(100), readonly=True)
        bridge.start()
        time.sleep(0.05)
        target.simulate(path, TagValue(99, IntVariant()))
        time.sleep(0.05)
        bridge.stop()
        written = source.written(path)
        self.assertFalse(
            written.present(),
            "BridgeSync readonly must not write back"
        )


class BridgeSyncUpdatesTargetWithFreshValuesTest(unittest.TestCase):
    """BridgeSync updates target with fresh values."""

    def test(self):
        path = NodePath(["Sim", "Changing"])
        values = {path.text(): TagValue(1, IntVariant())}
        source = FakeDaSource([path], values)
        target = FakeUaTarget()
        bridge = BridgeSync(source, target, Milliseconds(30))
        bridge.start()
        time.sleep(0.05)
        newcontent = random.randint(100, 200)
        source.inject(path, TagValue(newcontent, IntVariant()))
        time.sleep(0.1)
        bridge.stop()
        reading = target.reading(path)
        self.assertEqual(
            reading.content().value().content(),
            newcontent,
            "BridgeSync must update target with fresh values"
        )


if __name__ == "__main__":
    unittest.main()
