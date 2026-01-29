# -*- coding: utf-8 -*-
"""
FakeMqttBroker for testing.

Example:
    >>> broker = FakeMqttBroker()
    >>> broker.connect()
    >>> broker.publish("topic/path", '{"value": 42}')
    >>> broker.messages()
    [('topic/path', '{"value": 42}')]
"""
from __future__ import print_function

import threading

from opcda_to_mqtt.mqtt.broker import (
    MqttBroker, Connected, Published, Disconnected
)
from opcda_to_mqtt.result.either import Right


class FakeMqttBroker(MqttBroker):
    """
    Test double for MqttBroker.

    Records all published messages for verification.
    Thread-safe for concurrent testing.

    Example:
        >>> broker = FakeMqttBroker()
        >>> broker.connect().is_right()
        True
        >>> broker.publish("t", "m").is_right()
        True
        >>> broker.messages()
        [('t', 'm')]
    """

    def __init__(self):
        """
        Create a FakeMqttBroker.

        Initializes empty message list and lock.
        """
        self._messages = []
        self._lock = threading.Lock()

    def connect(self):
        """
        Simulate successful connection.

        Returns:
            Right containing Connected marker
        """
        return Right(Connected())

    def publish(self, topic, message):
        """
        Record a published message.

        Args:
            topic: MQTT topic string
            message: Message content string

        Returns:
            Right containing Published marker
        """
        with self._lock:
            self._messages.append((topic, message))
        return Right(Published())

    def disconnect(self):
        """
        Simulate successful disconnection.

        Returns:
            Right containing Disconnected marker
        """
        return Right(Disconnected())

    def messages(self):
        """
        Get all recorded messages.

        Returns:
            List of (topic, message) tuples
        """
        with self._lock:
            return list(self._messages)

    def clear(self):
        """
        Clear all recorded messages.
        """
        with self._lock:
            self._messages = []
