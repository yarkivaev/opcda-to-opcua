# -*- coding: utf-8 -*-
"""
Memory profiling tests for verifying leak fixes.

These tests measure actual memory consumption to verify
that the memory leak fixes are working correctly.
"""
from __future__ import absolute_import
from __future__ import print_function

import gc
import logging
import random
import resource
import time
import types
import unittest

from opcda_to_mqtt.sync.bridge import Bridge
from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.timer import TimerThread
from opcda_to_mqtt.sync.worker import FakeWorker
from opcda_to_mqtt.mqtt.fake import FakeMqttBroker
from opcda_to_mqtt.domain.path import TagPath
from opcda_to_mqtt.domain.interval import Milliseconds

logging.disable(logging.CRITICAL)


class TestMemoryLeaks(unittest.TestCase):
    """Tests for memory leak verification."""

    def test_bridge_does_not_leak_function_objects(self):
        gc.collect()
        before = len([o for o in gc.get_objects() if isinstance(o, types.FunctionType)])
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {"Tag": random.randint(1, 100)})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(5), "t")
        time.sleep(0.2)
        bridge.stop()
        gc.collect()
        after = len([o for o in gc.get_objects() if isinstance(o, types.FunctionType)])
        growth = after - before
        self.assertLess(
            growth,
            50,
            "Function objects should not grow unboundedly, grew by %d" % growth
        )

    def test_bridge_memory_stays_stable_over_cycles(self):
        gc.collect()
        before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        readings = {"Tag1": random.randint(1, 100), "Tag2": random.randint(1, 100)}
        worker = FakeWorker(queue, readings)
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag1"), TagPath("Tag2")], Milliseconds(5), "t")
        time.sleep(0.5)
        bridge.stop()
        gc.collect()
        after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        growth_kb = (after - before) / 1024
        self.assertLess(
            growth_kb,
            1024,
            "Memory growth should be less than 1MB, grew by %d KB" % growth_kb
        )

    def test_tag_count_matches_path_count(self):
        gc.collect()
        count = random.randint(5, 15)
        paths = [TagPath("Tag%d" % i) for i in range(count)]
        readings = {path.text(): random.randint(1, 100) for path in paths}
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, readings)
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start(paths, Milliseconds(5), "t")
        time.sleep(0.1)
        bridge.stop()
        gc.collect()
        tags = [o for o in gc.get_objects() if type(o).__name__ == "Tag"]
        self.assertLessEqual(
            len(tags),
            count + 5,
            "Tag count should match path count not cycle count"
        )

    def test_lambda_count_stable_over_many_cycles(self):
        gc.collect()
        before = len([o for o in gc.get_objects()
                      if type(o).__name__ == "function" and getattr(o, "__closure__", None)])
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {"Tag": random.randint(1, 100)})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(2), "t")
        time.sleep(3.0)
        bridge.stop()
        gc.collect()
        after = len([o for o in gc.get_objects()
                     if type(o).__name__ == "function" and getattr(o, "__closure__", None)])
        growth = after - before
        self.assertLess(
            growth,
            20,
            "Lambda count should stay bounded, grew by %d" % growth
        )


if __name__ == "__main__":
    unittest.main()
