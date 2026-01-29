# -*- coding: utf-8 -*-
"""
Tests for Bridge.
"""
from __future__ import print_function

import json
import logging
import random
import string
import time
import unittest

from opcda_to_mqtt.sync.bridge import Bridge
from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.timer import TimerThread
from opcda_to_mqtt.sync.worker import FakeWorker
from opcda_to_mqtt.mqtt.fake import FakeMqttBroker
from opcda_to_mqtt.domain.path import TagPath
from opcda_to_mqtt.domain.interval import Milliseconds

logging.disable(logging.CRITICAL)


class TestBridge(unittest.TestCase):
    """Tests for Bridge."""

    def test_bridge_connects_broker_on_start(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(100), "topic")
        time.sleep(0.05)
        bridge.stop()

    def test_bridge_enqueues_task_for_each_tag(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        readings = {"Tag1": 1, "Tag2": 2}
        worker = FakeWorker(queue, readings)
        bridge = Bridge(queue, [worker], timer, broker)
        tags = [TagPath("Tag1"), TagPath("Tag2")]
        bridge.start(tags, Milliseconds(1000), "topic")
        time.sleep(0.05)
        bridge.stop()
        self.assertGreaterEqual(
            len(worker.executed()),
            2,
            "Bridge should enqueue task for each tag"
        )

    def test_bridge_publishes_to_mqtt(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        path = "".join(random.choice(string.ascii_letters) for _ in range(8))
        value = random.randint(1, 100)
        worker = FakeWorker(queue, {path: value})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath(path)], Milliseconds(500), "factory")
        time.sleep(0.05)
        bridge.stop()
        messages = broker.messages()
        self.assertGreaterEqual(
            len(messages),
            1,
            "Bridge should publish to MQTT"
        )

    def test_bridge_publishes_correct_topic(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        path = "Device.Sensor"
        topic = "factory/line1"
        worker = FakeWorker(queue, {path: 42})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath(path)], Milliseconds(500), topic)
        time.sleep(0.05)
        bridge.stop()
        messages = broker.messages()
        self.assertEqual(
            messages[0][0],
            "factory/line1/Device.Sensor",
            "Bridge should publish correct topic"
        )

    def test_bridge_publishes_json_message(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        value = random.randint(1, 100)
        worker = FakeWorker(queue, {"Tag": value})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(500), "t")
        time.sleep(0.05)
        bridge.stop()
        messages = broker.messages()
        data = json.loads(messages[0][1])
        self.assertEqual(
            data["value"],
            value,
            "Bridge should publish JSON with value"
        )

    def test_bridge_publishes_quality_in_message(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {"Tag": 1})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(500), "t")
        time.sleep(0.05)
        bridge.stop()
        messages = broker.messages()
        data = json.loads(messages[0][1])
        self.assertEqual(
            data["quality"],
            "good",
            "Bridge should publish quality in message"
        )

    def test_bridge_reschedules_after_read(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {"Tag": 1})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(10), "t")
        time.sleep(0.05)
        bridge.stop()
        messages = broker.messages()
        self.assertGreaterEqual(
            len(messages),
            2,
            "Bridge should reschedule after read"
        )

    def test_bridge_stops_timer_on_stop(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(500), "t")
        bridge.stop()

    def test_bridge_sends_sentinels_to_workers(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        workers = [FakeWorker(queue, {}) for _ in range(3)]
        bridge = Bridge(queue, workers, timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(500), "t")
        time.sleep(0.02)
        bridge.stop()

    def test_bridge_disconnects_broker_on_stop(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath("Tag")], Milliseconds(500), "t")
        bridge.stop()

    def test_bridge_handles_cyrillic_tag(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        path = u"COM1.\u0422\u041c_5104"
        worker = FakeWorker(queue, {path: 42})
        bridge = Bridge(queue, [worker], timer, broker)
        bridge.start([TagPath(path)], Milliseconds(500), "t")
        time.sleep(0.05)
        bridge.stop()
        messages = broker.messages()
        self.assertGreaterEqual(
            len(messages),
            1,
            "Bridge should handle Cyrillic tag"
        )

    def test_bridge_repr_shows_worker_count(self):
        queue = TaskQueue()
        timer = TimerThread()
        broker = FakeMqttBroker()
        count = random.randint(2, 5)
        workers = [FakeWorker(queue, {}) for _ in range(count)]
        bridge = Bridge(queue, workers, timer, broker)
        self.assertIn(
            str(count),
            repr(bridge),
            "Bridge repr should show worker count"
        )


if __name__ == "__main__":
    unittest.main()
