# -*- coding: utf-8 -*-
"""
Reading abstraction for OPC data with timestamp and quality.

Reading represents a complete OPC data point including value,
quality, and timestamp information.

Example usage:
    reading = OpcReading(path, value, quality, timestamp)
    if reading.quality().good():
        print(reading.value().content())
"""
import time
from abc import ABC, abstractmethod


class Reading(ABC):
    """
    Interface for OPC reading representation.

    Reading encapsulates a complete OPC data point with
    value, quality, and timestamp.
    """

    @abstractmethod
    def path(self):
        """
        Extract the node path.

        Returns:
            Path: The source node path
        """
        pass

    @abstractmethod
    def value(self):
        """
        Extract the data value.

        Returns:
            Value: The reading value
        """
        pass

    @abstractmethod
    def quality(self):
        """
        Extract the data quality.

        Returns:
            Quality: The reading quality
        """
        pass

    @abstractmethod
    def timestamp(self):
        """
        Extract the timestamp.

        Returns:
            Timestamp: When the reading was taken
        """
        pass


class OpcReading(Reading):
    """
    Immutable OPC reading with full metadata.

    OpcReading encapsulates a complete data point from an
    OPC server, including path, value, quality, and timestamp.

    Example usage:
        reading = OpcReading(path, value, quality, timestamp)
        print(reading.value().content())
    """

    def __init__(self, path, value, quality, timestamp):
        """
        Create OpcReading with all components.

        Args:
            path (Path): Source node path
            value (Value): Reading value
            quality (Quality): Reading quality
            timestamp (Timestamp): Reading timestamp
        """
        self._path = path
        self._value = value
        self._quality = quality
        self._timestamp = timestamp

    def path(self):
        """
        Extract the node path.

        Returns:
            Path: The source node path
        """
        return self._path

    def value(self):
        """
        Extract the data value.

        Returns:
            Value: The reading value
        """
        return self._value

    def quality(self):
        """
        Extract the data quality.

        Returns:
            Quality: The reading quality
        """
        return self._quality

    def timestamp(self):
        """
        Extract the timestamp.

        Returns:
            Timestamp: When the reading was taken
        """
        return self._timestamp


class Timestamp(object):
    """
    Immutable timestamp representation.

    Timestamp encapsulates a point in time, compatible with
    Python 3.4 (no datetime.timestamp() method).

    Example usage:
        ts = Timestamp(time.time())
        print(ts.epoch())  # Epoch seconds
        print(ts.text())  # ISO format string
    """

    def __init__(self, epoch):
        """
        Create timestamp from epoch seconds.

        Args:
            epoch (float): Seconds since Unix epoch
        """
        self._epoch = epoch

    def epoch(self):
        """
        Extract epoch seconds.

        Returns:
            float: Seconds since Unix epoch
        """
        return self._epoch

    def text(self):
        """
        Format as ISO 8601 string.

        Returns:
            str: Formatted timestamp string
        """
        return time.strftime(
            "%Y-%m-%dT%H:%M:%S",
            time.localtime(self._epoch)
        )


class TimestampNow(Timestamp):
    """
    Timestamp for current time.

    Example usage:
        ts = TimestampNow()
        print(ts.epoch())  # Current epoch time
    """

    def __init__(self):
        """Create timestamp for current time."""
        Timestamp.__init__(self, time.time())
