# -*- coding: utf-8 -*-
"""
Tests for Tag.
"""
from __future__ import print_function

import logging
import random
import string
import time
import unittest

from opcda_to_mqtt.domain.tag import Tag
from opcda_to_mqtt.domain.path import TagPath
from opcda_to_mqtt.domain.interval import Milliseconds
from opcda_to_mqtt.sync.schedule import Schedule
from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.timer import TimerThread
from opcda_to_mqtt.mqtt.fake import FakeMqttBroker
from opcda_to_mqtt.sync.worker import FakeOpcClient

logging.disable(logging.CRITICAL)


class TestTag(unittest.TestCase):
    """Tests for Tag."""

    def test_tag_path_returns_configured_path(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        name = "".join(random.choice(string.ascii_letters) for _ in range(8))
        path = TagPath(name)
        tag = Tag(path, broker, "topic", schedule)
        self.assertEqual(
            tag.path(),
            path,
            "Tag path should return configured path"
        )

    def test_tag_reading_returns_tag_read(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        path = TagPath("Device.Temp")
        tag = Tag(path, broker, "factory", schedule)
        source = FakeOpcClient({})
        reading = tag.reading(source)
        self.assertEqual(
            type(reading).__name__,
            "TagRead",
            "Tag reading should return TagRead"
        )

    def test_tag_reading_publishes_to_broker(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        name = "".join(random.choice(string.ascii_letters) for _ in range(6))
        path = TagPath(name)
        value = random.randint(1, 100)
        tag = Tag(path, broker, "t", schedule)
        source = FakeOpcClient({name: value})
        broker.connect()
        timer.start()
        tag.reading(source).publish()
        time.sleep(0.05)
        timer.stop()
        messages = broker.messages()
        self.assertGreaterEqual(
            len(messages),
            1,
            "Tag reading should publish to broker"
        )

    def test_tag_reading_reschedules_tag(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(random.randint(5, 15)), queue)
        broker = FakeMqttBroker()
        path = TagPath("Sensor")
        tag = Tag(path, broker, "t", schedule)
        source = FakeOpcClient({"Sensor": 42})
        broker.connect()
        timer.start()
        tag.reading(source).publish()
        time.sleep(0.1)
        timer.stop()
        result = queue.get()
        self.assertIs(
            result,
            tag,
            "Tag reading should reschedule same tag"
        )

    def test_tag_reading_publishes_correct_topic(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        path = TagPath("Device.Sensor")
        topic = "factory/line"
        tag = Tag(path, broker, topic, schedule)
        source = FakeOpcClient({"Device.Sensor": 1})
        broker.connect()
        timer.start()
        tag.reading(source).publish()
        timer.stop()
        messages = broker.messages()
        self.assertEqual(
            messages[0][0],
            "factory/line/Device.Sensor",
            "Tag reading should publish to correct topic"
        )

    def test_tag_repr_shows_path(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        name = "".join(random.choice(string.ascii_letters) for _ in range(8))
        path = TagPath(name)
        tag = Tag(path, broker, "t", schedule)
        self.assertIn(
            name,
            repr(tag),
            "Tag repr should show path"
        )

    def test_tag_handles_cyrillic_path(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        broker = FakeMqttBroker()
        name = u"COM1.\u0422\u041c_5104"
        path = TagPath(name)
        tag = Tag(path, broker, "t", schedule)
        source = FakeOpcClient({name: random.randint(1, 100)})
        broker.connect()
        timer.start()
        tag.reading(source).publish()
        timer.stop()
        messages = broker.messages()
        self.assertGreaterEqual(
            len(messages),
            1,
            "Tag should handle Cyrillic path"
        )


if __name__ == "__main__":
    unittest.main()
