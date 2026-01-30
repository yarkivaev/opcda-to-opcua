# -*- coding: utf-8 -*-
"""
Tag domain object for OPC-DA to MQTT publishing.

Example:
    >>> tag = Tag(TagPath("Device.Temp"), broker, "factory", schedule)
    >>> tag.path().text()
    'Device.Temp'
    >>> tag.reading(source).publish()
"""
from __future__ import print_function

from opcda_to_mqtt.sync.reading import TagRead


class Tag(object):
    """
    Immutable tag that produces readings.

    Holds path and publishing/scheduling dependencies.
    Four attributes: path, broker, topic, schedule.

    Example:
        >>> tag = Tag(path, broker, topic, schedule)
        >>> reading = tag.reading(source)
        >>> reading.publish()  # Reads, publishes, reschedules
    """

    def __init__(self, path, broker, topic, schedule):
        """
        Create a Tag.

        Args:
            path: TagPath for this tag
            broker: MqttBroker for publishing
            topic: Base topic prefix string
            schedule: Schedule for re-enqueueing
        """
        self._path = path
        self._broker = broker
        self._topic = topic
        self._schedule = schedule

    def path(self):
        """
        Get the tag path.

        Returns:
            TagPath for this tag
        """
        return self._path

    def reading(self, source):
        """
        Create a reading from this tag.

        Args:
            source: OPC client for reading values

        Returns:
            TagRead that can publish itself
        """
        return TagRead(self._path, source, self._output, self._later)

    def _output(self, message):
        """
        Publish message to MQTT.

        Args:
            message: JSON message string
        """
        self._broker.publish(self._path.topic(self._topic), message)

    def _later(self):
        """
        Schedule this tag for re-enqueueing.
        """
        self._schedule.later(self)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Tag and its path
        """
        return "Tag(%r)" % self._path
