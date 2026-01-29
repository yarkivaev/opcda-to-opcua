# -*- coding: utf-8 -*-
"""
Tests for MqttBroker and FakeMqttBroker.
"""
from __future__ import print_function

import logging
import random
import string
import threading
import unittest

from opcda_to_mqtt.mqtt.fake import FakeMqttBroker
from opcda_to_mqtt.mqtt.broker import Connected, Published, Disconnected

logging.disable(logging.CRITICAL)


class TestFakeMqttBroker(unittest.TestCase):
    """Tests for FakeMqttBroker."""

    def test_fake_broker_connect_returns_right(self):
        broker = FakeMqttBroker()
        result = broker.connect()
        self.assertTrue(
            result.is_right(),
            "FakeMqttBroker.connect should return Right"
        )

    def test_fake_broker_connect_returns_connected(self):
        broker = FakeMqttBroker()
        result = broker.connect()
        marker = result.fold(lambda e: "error", lambda c: c)
        self.assertEqual(
            marker,
            Connected(),
            "FakeMqttBroker.connect should return Connected"
        )

    def test_fake_broker_publish_returns_right(self):
        broker = FakeMqttBroker()
        result = broker.publish("topic", "message")
        self.assertTrue(
            result.is_right(),
            "FakeMqttBroker.publish should return Right"
        )

    def test_fake_broker_publish_returns_published(self):
        broker = FakeMqttBroker()
        result = broker.publish("t", "m")
        marker = result.fold(lambda e: "error", lambda p: p)
        self.assertEqual(
            marker,
            Published(),
            "FakeMqttBroker.publish should return Published"
        )

    def test_fake_broker_disconnect_returns_right(self):
        broker = FakeMqttBroker()
        result = broker.disconnect()
        self.assertTrue(
            result.is_right(),
            "FakeMqttBroker.disconnect should return Right"
        )

    def test_fake_broker_disconnect_returns_disconnected(self):
        broker = FakeMqttBroker()
        result = broker.disconnect()
        marker = result.fold(lambda e: "error", lambda d: d)
        self.assertEqual(
            marker,
            Disconnected(),
            "FakeMqttBroker.disconnect should return Disconnected"
        )

    def test_fake_broker_messages_starts_empty(self):
        broker = FakeMqttBroker()
        self.assertEqual(
            len(broker.messages()),
            0,
            "FakeMqttBroker should start with empty messages"
        )

    def test_fake_broker_records_published_message(self):
        broker = FakeMqttBroker()
        topic = "".join(random.choice(string.ascii_letters) for _ in range(8))
        message = "".join(random.choice(string.ascii_letters) for _ in range(12))
        broker.publish(topic, message)
        messages = broker.messages()
        self.assertEqual(
            messages[0],
            (topic, message),
            "FakeMqttBroker should record published message"
        )

    def test_fake_broker_records_multiple_messages(self):
        broker = FakeMqttBroker()
        count = random.randint(3, 10)
        for i in range(count):
            broker.publish("topic%d" % i, "msg%d" % i)
        self.assertEqual(
            len(broker.messages()),
            count,
            "FakeMqttBroker should record multiple messages"
        )

    def test_fake_broker_clear_removes_messages(self):
        broker = FakeMqttBroker()
        broker.publish("t", "m")
        broker.clear()
        self.assertEqual(
            len(broker.messages()),
            0,
            "FakeMqttBroker.clear should remove messages"
        )

    def test_fake_broker_messages_returns_copy(self):
        broker = FakeMqttBroker()
        broker.publish("t", "m")
        returned = broker.messages()
        returned.append(("new", "msg"))
        self.assertEqual(
            len(broker.messages()),
            1,
            "FakeMqttBroker.messages should return a copy"
        )

    def test_fake_broker_handles_cyrillic_message(self):
        broker = FakeMqttBroker()
        message = u"\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435"
        broker.publish("topic", message)
        messages = broker.messages()
        self.assertEqual(
            messages[0][1],
            message,
            "FakeMqttBroker should handle Cyrillic message"
        )

    def test_fake_broker_is_thread_safe(self):
        broker = FakeMqttBroker()
        threads = []
        for i in range(10):
            t = threading.Thread(
                target=lambda n=i: broker.publish("topic", "msg%d" % n)
            )
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(
            len(broker.messages()),
            10,
            "FakeMqttBroker should be thread-safe"
        )


class TestMarkers(unittest.TestCase):
    """Tests for marker classes."""

    def test_connected_equals_another_connected(self):
        self.assertEqual(
            Connected(),
            Connected(),
            "Connected markers should be equal"
        )

    def test_published_equals_another_published(self):
        self.assertEqual(
            Published(),
            Published(),
            "Published markers should be equal"
        )

    def test_disconnected_equals_another_disconnected(self):
        self.assertEqual(
            Disconnected(),
            Disconnected(),
            "Disconnected markers should be equal"
        )

    def test_connected_repr(self):
        self.assertEqual(
            repr(Connected()),
            "Connected()",
            "Connected repr should be Connected()"
        )

    def test_published_repr(self):
        self.assertEqual(
            repr(Published()),
            "Published()",
            "Published repr should be Published()"
        )

    def test_disconnected_repr(self):
        self.assertEqual(
            repr(Disconnected()),
            "Disconnected()",
            "Disconnected repr should be Disconnected()"
        )


if __name__ == "__main__":
    unittest.main()
