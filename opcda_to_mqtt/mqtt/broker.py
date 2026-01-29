# -*- coding: utf-8 -*-
"""
MqttBroker interface for publishing messages.

Example:
    >>> broker = FakeMqttBroker()
    >>> broker.connect()
    >>> broker.publish("topic", "message")
    >>> broker.disconnect()
"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod


class MqttBroker:
    """
    Interface for MQTT message publishing.

    Implementations connect to MQTT brokers and publish messages.

    Example:
        >>> class MyBroker(MqttBroker):
        ...     def connect(self):
        ...         return Right(Connected())
        ...     def publish(self, topic, message):
        ...         return Right(Published())
        ...     def disconnect(self):
        ...         return Right(Disconnected())
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self):
        """
        Connect to the MQTT broker.

        Returns:
            Either[Problem, Connected]
        """
        raise NotImplementedError()

    @abstractmethod
    def publish(self, topic, message):
        """
        Publish a message to a topic.

        Args:
            topic: MQTT topic string
            message: Message content string

        Returns:
            Either[Problem, Published]
        """
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self):
        """
        Disconnect from the MQTT broker.

        Returns:
            Either[Problem, Disconnected]
        """
        raise NotImplementedError()


class Connected:
    """
    Marker indicating successful connection.

    Example:
        >>> c = Connected()
        >>> repr(c)
        'Connected()'
    """

    def __eq__(self, other):
        """
        Check equality with another Connected.

        Args:
            other: Object to compare

        Returns:
            True if other is Connected
        """
        return isinstance(other, Connected)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Connected
        """
        return "Connected()"


class Published:
    """
    Marker indicating successful publish.

    Example:
        >>> p = Published()
        >>> repr(p)
        'Published()'
    """

    def __eq__(self, other):
        """
        Check equality with another Published.

        Args:
            other: Object to compare

        Returns:
            True if other is Published
        """
        return isinstance(other, Published)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Published
        """
        return "Published()"


class Disconnected:
    """
    Marker indicating successful disconnection.

    Example:
        >>> d = Disconnected()
        >>> repr(d)
        'Disconnected()'
    """

    def __eq__(self, other):
        """
        Check equality with another Disconnected.

        Args:
            other: Object to compare

        Returns:
            True if other is Disconnected
        """
        return isinstance(other, Disconnected)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Disconnected
        """
        return "Disconnected()"
