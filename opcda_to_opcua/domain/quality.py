# -*- coding: utf-8 -*-
"""
Quality abstraction for OPC data quality indicators.

Quality represents the reliability and validity of an OPC value.
OPC DA defines quality codes: Good (192+), Bad (0-63), Uncertain (64-191).

Example usage:
    quality = OpcQuality(192)
    if quality.good():
        print("Data is reliable")
"""
from abc import ABC, abstractmethod


class Quality(ABC):
    """
    Interface for OPC quality representation.

    Quality encapsulates the OPC DA quality code without exposing
    the raw numeric value. Implementations must be immutable.
    """

    @abstractmethod
    def code(self):
        """
        Extract the numeric quality code.

        Returns:
            int: OPC DA quality code (0-255)
        """
        pass

    @abstractmethod
    def good(self):
        """
        Query whether quality indicates good data.

        Returns:
            bool: True if quality code indicates good data
        """
        pass

    @abstractmethod
    def bad(self):
        """
        Query whether quality indicates bad data.

        Returns:
            bool: True if quality code indicates bad data
        """
        pass

    @abstractmethod
    def uncertain(self):
        """
        Query whether quality indicates uncertain data.

        Returns:
            bool: True if quality code indicates uncertain data
        """
        pass


class OpcQuality(Quality):
    """
    OPC DA quality code implementation.

    OpcQuality interprets OPC DA quality codes according to the
    OPC DA specification:
    - Bad: 0-63
    - Uncertain: 64-191
    - Good: 192-255

    Example usage:
        good = OpcQuality(192)
        print(good.good())  # True

        bad = OpcQuality(0)
        print(bad.bad())  # True
    """

    def __init__(self, code):
        """
        Create OpcQuality from quality code.

        Args:
            code (int): OPC DA quality code (0-255)
        """
        self._code = code

    def code(self):
        """
        Extract the numeric quality code.

        Returns:
            int: OPC DA quality code
        """
        return self._code

    def good(self):
        """
        Query whether quality indicates good data.

        Good quality codes are 192-255 (top 2 bits = 11).

        Returns:
            bool: True if code >= 192
        """
        return self._code >= 192

    def bad(self):
        """
        Query whether quality indicates bad data.

        Bad quality codes are 0-63 (top 2 bits = 00).

        Returns:
            bool: True if code < 64
        """
        return self._code < 64

    def uncertain(self):
        """
        Query whether quality indicates uncertain data.

        Uncertain quality codes are 64-191 (top 2 bits = 01 or 10).

        Returns:
            bool: True if 64 <= code < 192
        """
        return 64 <= self._code < 192

    def __eq__(self, other):
        """
        Compare quality codes for equality.

        Args:
            other: Another quality to compare

        Returns:
            bool: True if codes match
        """
        if not isinstance(other, OpcQuality):
            return False
        return self._code == other._code

    def __hash__(self):
        """
        Compute hash for use in collections.

        Returns:
            int: Hash based on code
        """
        return hash(self._code)
