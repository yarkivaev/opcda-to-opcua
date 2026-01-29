# -*- coding: utf-8 -*-
"""
Milliseconds domain object representing a time interval.

Example:
    >>> interval = Milliseconds(500)
    >>> interval.seconds()
    0.5
"""
from __future__ import print_function


class Milliseconds:
    """
    Immutable time interval in milliseconds.

    Represents a duration for polling or delays.

    Example:
        >>> Milliseconds(1000).seconds()
        1.0
        >>> Milliseconds(500).amount()
        500
    """

    def __init__(self, amount):
        """
        Create a Milliseconds interval.

        Args:
            amount: Number of milliseconds (must be positive)

        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Milliseconds must be positive")
        self._amount = amount

    def amount(self):
        """
        Get the raw milliseconds value.

        Returns:
            Number of milliseconds as integer
        """
        return self._amount

    def seconds(self):
        """
        Convert to seconds.

        Returns:
            Number of seconds as float
        """
        return self._amount / 1000.0

    def __eq__(self, other):
        """
        Check equality with another Milliseconds.

        Args:
            other: Object to compare

        Returns:
            True if other is Milliseconds with same amount
        """
        if not isinstance(other, Milliseconds):
            return False
        return self._amount == other._amount

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Milliseconds and its amount
        """
        return "Milliseconds(%d)" % self._amount
