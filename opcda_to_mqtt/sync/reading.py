# -*- coding: utf-8 -*-
"""
TagRead for executing tag reads and publishing.

Example:
    >>> reading = TagRead(path, source, output, reschedule)
    >>> reading.publish()  # Reads, publishes, reschedules
"""
from __future__ import print_function

import json

from opcda_to_mqtt.domain.value import TagValue
from opcda_to_mqtt.domain.quality import OpcQuality


class TagRead(object):
    """
    Executable reading that publishes itself.

    Reads from source, formats JSON, publishes, reschedules.
    Four attributes: path, source, output, reschedule.

    Example:
        >>> reading = TagRead(path, source, output_fn, reschedule_fn)
        >>> reading.publish()
    """

    def __init__(self, path, source, output, reschedule):
        """
        Create a TagRead.

        Args:
            path: TagPath to read
            source: OPC client for reading
            output: Callable to publish message
            reschedule: Callable to schedule next read
        """
        self._path = path
        self._source = source
        self._output = output
        self._reschedule = reschedule

    def publish(self):
        """
        Read tag, publish to MQTT, schedule next read.
        """
        result = self._source.read(self._path.text(), sync=True)
        value, quality, _ = result
        message = json.dumps({
            "value": TagValue(value).json(),
            "quality": OpcQuality(quality).text()
        })
        self._output(message)
        self._reschedule()

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing TagRead and its path
        """
        return "TagRead(%r)" % self._path
