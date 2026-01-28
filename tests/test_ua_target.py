# -*- coding: utf-8 -*-
"""
Unit tests for FakeUaTarget.
"""
import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.ua.fake import FakeUaTarget
from opcda_to_opcua.domain.path import NodePath
from opcda_to_opcua.domain.value import TagValue
from opcda_to_opcua.domain.variant import IntVariant
from opcda_to_opcua.domain.quality import OpcQuality
from opcda_to_opcua.domain.reading import OpcReading, TimestampNow
from opcda_to_opcua.domain.node import DaReadableNode


class FakeUaTargetStartsSuccessfullyTest(unittest.TestCase):
    """FakeUaTarget starts successfully."""

    def test(self):
        target = FakeUaTarget()
        result = target.start()
        self.assertTrue(
            result.successful(),
            "FakeUaTarget must start successfully"
        )


class FakeUaTargetStopsSuccessfullyTest(unittest.TestCase):
    """FakeUaTarget stops successfully."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        result = target.stop()
        self.assertTrue(
            result.successful(),
            "FakeUaTarget must stop successfully"
        )


class FakeUaTargetFailsMirrorWhenNotRunningTest(unittest.TestCase):
    """FakeUaTarget fails mirror when not running."""

    def test(self):
        target = FakeUaTarget()
        result = target.mirror([])
        self.assertFalse(
            result.successful(),
            "FakeUaTarget must fail mirror when not running"
        )


class FakeUaTargetMirrorsNodesTest(unittest.TestCase):
    """FakeUaTarget mirrors nodes."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        nodes = [object(), object()]
        result = target.mirror(nodes)
        self.assertTrue(
            result.successful(),
            "FakeUaTarget must mirror nodes successfully"
        )


class FakeUaTargetRecordsMirroredNodesTest(unittest.TestCase):
    """FakeUaTarget records mirrored nodes."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        nodes = [object(), object()]
        target.mirror(nodes)
        mirrored = target.mirrored()
        self.assertEqual(
            len(mirrored),
            2,
            "FakeUaTarget must record mirrored nodes"
        )


class FakeUaTargetUpdatesReadingTest(unittest.TestCase):
    """FakeUaTarget updates reading."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        path = NodePath(["Sim", "Tag%d" % random.randint(1, 100)])
        value = TagValue(random.randint(1, 100), IntVariant())
        reading = OpcReading(path, value, OpcQuality(192), TimestampNow())
        result = target.update(path, reading)
        self.assertTrue(
            result.successful(),
            "FakeUaTarget must update reading successfully"
        )


class FakeUaTargetRecordsUpdatedReadingTest(unittest.TestCase):
    """FakeUaTarget records updated reading."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        path = NodePath(["Sim", "Tag"])
        content = random.randint(1, 100)
        value = TagValue(content, IntVariant())
        reading = OpcReading(path, value, OpcQuality(192), TimestampNow())
        target.update(path, reading)
        recorded = target.reading(path)
        self.assertEqual(
            recorded.content().value().content(),
            content,
            "FakeUaTarget must record updated reading"
        )


class FakeUaTargetReadingReturnsEmptyForUnupdatedTest(unittest.TestCase):
    """FakeUaTarget reading returns Empty for unupdated path."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        path = NodePath(["Sim", "Unupdated"])
        recorded = target.reading(path)
        self.assertFalse(
            recorded.present(),
            "FakeUaTarget reading must return Empty for unupdated path"
        )


class FakeUaTargetFailsUpdateWhenNotRunningTest(unittest.TestCase):
    """FakeUaTarget fails update when not running."""

    def test(self):
        target = FakeUaTarget()
        path = NodePath(["Sim", "Tag"])
        value = TagValue(42, IntVariant())
        reading = OpcReading(path, value, OpcQuality(192), TimestampNow())
        result = target.update(path, reading)
        self.assertFalse(
            result.successful(),
            "FakeUaTarget must fail update when not running"
        )


class FakeUaTargetSubscribesCallbackTest(unittest.TestCase):
    """FakeUaTarget subscribes callback."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        callback = object()
        result = target.subscribe(callback)
        self.assertTrue(
            result.successful(),
            "FakeUaTarget must subscribe callback successfully"
        )


class FakeUaTargetFailsSubscribeWhenNotRunningTest(unittest.TestCase):
    """FakeUaTarget fails subscribe when not running."""

    def test(self):
        target = FakeUaTarget()
        callback = object()
        result = target.subscribe(callback)
        self.assertFalse(
            result.successful(),
            "FakeUaTarget must fail subscribe when not running"
        )


class FakeUaTargetSimulatesWriteTest(unittest.TestCase):
    """FakeUaTarget simulates write calling callback."""

    def test(self):
        target = FakeUaTarget()
        target.start()
        called = [False]
        class TestCallback:
            def handle(self, path, value):
                called[0] = True
        target.subscribe(TestCallback())
        path = NodePath(["Sim", "Setpoint"])
        value = TagValue(random.randint(1, 100), IntVariant())
        target.simulate(path, value)
        self.assertTrue(
            called[0],
            "FakeUaTarget simulate must call callback"
        )


if __name__ == "__main__":
    unittest.main()
