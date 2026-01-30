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

    Holds path and cached callbacks for publishing and scheduling.
    Four attributes: path, enqueue, output, later.

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
        self._enqueue = lambda: schedule.enqueue(self)
        self._output_bound = lambda m: broker.publish(path.topic(topic), m)
        self._later_bound = lambda: schedule.later(self._enqueue)

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
        return TagRead(self._path, source, self._output_bound, self._later_bound)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Tag and its path
        """
        return "Tag(%r)" % self._path
