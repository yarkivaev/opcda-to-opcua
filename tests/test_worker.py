# -*- coding: utf-8 -*-
"""
Tests for Worker and FakeWorker.
"""
from __future__ import print_function

import logging
import random
import string
import time
import unittest

from opcda_to_mqtt.sync.worker import FakeWorker, FakeOpcClient
from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.timer import TimerThread
from opcda_to_mqtt.sync.schedule import Schedule
from opcda_to_mqtt.domain.tag import Tag
from opcda_to_mqtt.domain.path import TagPath
from opcda_to_mqtt.domain.interval import Milliseconds
from opcda_to_mqtt.mqtt.fake import FakeMqttBroker

logging.disable(logging.CRITICAL)


class TestFakeWorker(unittest.TestCase):
    """Tests for FakeWorker."""

    def test_worker_starts_with_no_executed(self):
        queue = TaskQueue()
        worker = FakeWorker(queue, {})
        self.assertEqual(
            len(worker.executed()),
            0,
            "FakeWorker should start with no executed"
        )

    def test_worker_executes_tag_from_queue(self):
        queue = TaskQueue()
        timer = TimerThread()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        name = "".join(random.choice(string.ascii_letters) for _ in range(8))
        value = random.randint(1, 100)
        worker = FakeWorker(queue, {name: value})
        broker.connect()
        timer.start()
        worker.start()
        tag = Tag(TagPath(name), broker, "t", schedule)
        queue.put(tag)
        queue.put(None)
        worker.join()
        timer.stop()
        messages = broker.messages()
        self.assertGreaterEqual(
            len(messages),
            1,
            "FakeWorker should execute tag from queue"
        )

    def test_worker_records_executed_tags(self):
        queue = TaskQueue()
        timer = TimerThread()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {"Tag": 1})
        broker.connect()
        timer.start()
        worker.start()
        tag = Tag(TagPath("Tag"), broker, "t", schedule)
        queue.put(tag)
        queue.put(None)
        worker.join()
        timer.stop()
        self.assertEqual(
            len(worker.executed()),
            1,
            "FakeWorker should record executed tags"
        )

    def test_worker_stops_on_sentinel(self):
        queue = TaskQueue()
        worker = FakeWorker(queue, {})
        worker.start()
        queue.put(None)
        worker.join()

    def test_worker_executes_multiple_tags(self):
        queue = TaskQueue()
        timer = TimerThread()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        count = random.randint(3, 7)
        readings = {"Tag%d" % i: i for i in range(count)}
        worker = FakeWorker(queue, readings)
        broker.connect()
        timer.start()
        worker.start()
        for i in range(count):
            tag = Tag(TagPath("Tag%d" % i), broker, "t", schedule)
            queue.put(tag)
        queue.put(None)
        worker.join()
        timer.stop()
        self.assertEqual(
            len(worker.executed()),
            count,
            "FakeWorker should execute multiple tags"
        )

    def test_worker_uses_configured_readings(self):
        queue = TaskQueue()
        timer = TimerThread()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        name = "Device.Sensor"
        value = random.randint(1, 1000)
        worker = FakeWorker(queue, {name: value})
        broker.connect()
        timer.start()
        worker.start()
        tag = Tag(TagPath(name), broker, "t", schedule)
        queue.put(tag)
        queue.put(None)
        worker.join()
        timer.stop()
        messages = broker.messages()
        self.assertIn(
            str(value),
            messages[0][1],
            "FakeWorker should use configured readings"
        )

    def test_worker_handles_cyrillic_path(self):
        queue = TaskQueue()
        timer = TimerThread()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        name = u"COM1.\u0422\u041c_5104"
        value = random.randint(1, 100)
        worker = FakeWorker(queue, {name: value})
        broker.connect()
        timer.start()
        worker.start()
        tag = Tag(TagPath(name), broker, "t", schedule)
        queue.put(tag)
        queue.put(None)
        worker.join()
        timer.stop()
        messages = broker.messages()
        self.assertGreaterEqual(
            len(messages),
            1,
            "FakeWorker should handle Cyrillic path"
        )

    def test_worker_executed_returns_copy(self):
        queue = TaskQueue()
        timer = TimerThread()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        worker = FakeWorker(queue, {"Tag": 1})
        broker.connect()
        timer.start()
        worker.start()
        tag = Tag(TagPath("Tag"), broker, "t", schedule)
        queue.put(tag)
        queue.put(None)
        worker.join()
        timer.stop()
        executed = worker.executed()
        executed.append("extra")
        self.assertEqual(
            len(worker.executed()),
            1,
            "FakeWorker.executed should return a copy"
        )


class TestFakeOpcClient(unittest.TestCase):
    """Tests for FakeOpcClient."""

    def test_fake_client_read_returns_configured_value(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(8))
        value = random.randint(1, 1000)
        client = FakeOpcClient({path: value})
        result = client.read(path, sync=True)
        self.assertEqual(
            result[0],
            value,
            "FakeOpcClient.read should return configured value"
        )

    def test_fake_client_read_returns_good_quality(self):
        client = FakeOpcClient({"tag": 1})
        result = client.read("tag", sync=True)
        self.assertEqual(
            result[1],
            "Good",
            "FakeOpcClient.read should return Good quality"
        )

    def test_fake_client_read_returns_default_for_unknown(self):
        client = FakeOpcClient({})
        path = "".join(random.choice(string.ascii_letters) for _ in range(10))
        result = client.read(path, sync=True)
        self.assertEqual(
            result[0],
            0,
            "FakeOpcClient.read should return 0 for unknown tag"
        )

    def test_fake_client_connect_does_not_raise(self):
        client = FakeOpcClient({})
        client.connect("ProgID")

    def test_fake_client_close_does_not_raise(self):
        client = FakeOpcClient({})
        client.close()


if __name__ == "__main__":
    unittest.main()
