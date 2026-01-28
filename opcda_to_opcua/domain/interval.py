# -*- coding: utf-8 -*-
"""
Interval abstraction for time duration representation.

Interval represents a duration for polling or other timed operations.

Example usage:
    interval = Milliseconds(500)
    print(interval.milliseconds())  # 500
    print(interval.seconds())  # 0.5
"""
from abc import ABC, abstractmethod


class Interval(ABC):
    """
    Interface for time interval representation.

    Interval encapsulates a duration that can be expressed
    in various time units.
    """

    @abstractmethod
    def milliseconds(self):
        """
        Extract interval as milliseconds.

        Returns:
            int: Duration in milliseconds
        """
        pass

    @abstractmethod
    def seconds(self):
        """
        Extract interval as seconds.

        Returns:
            float: Duration in seconds
        """
        pass


class Milliseconds(Interval):
    """
    Interval specified in milliseconds.

    Example usage:
        interval = Milliseconds(500)
        print(interval.seconds())  # 0.5
    """

    def __init__(self, value):
        """
        Create interval from milliseconds.

        Args:
            value (int): Duration in milliseconds
        """
        self._value = value

    def milliseconds(self):
        """
        Extract as milliseconds.

        Returns:
            int: Duration in milliseconds
        """
        return self._value

    def seconds(self):
        """
        Convert to seconds.

        Returns:
            float: Duration in seconds
        """
        return self._value / 1000.0


class Seconds(Interval):
    """
    Interval specified in seconds.

    Example usage:
        interval = Seconds(2.5)
        print(interval.milliseconds())  # 2500
    """

    def __init__(self, value):
        """
        Create interval from seconds.

        Args:
            value (float): Duration in seconds
        """
        self._value = value

    def milliseconds(self):
        """
        Convert to milliseconds.

        Returns:
            int: Duration in milliseconds
        """
        return int(self._value * 1000)

    def seconds(self):
        """
        Extract as seconds.

        Returns:
            float: Duration in seconds
        """
        return self._value
