# -*- coding: utf-8 -*-
"""
OpcQuality domain object representing OPC quality code.

Example:
    >>> quality = OpcQuality("Good")
    >>> quality.text()
    'good'
    >>> quality.is_good()
    True
"""
from __future__ import print_function


class OpcQuality:
    """
    Immutable OPC quality code.

    Represents the quality of an OPC tag reading.
    Common values: "Good", "Bad", "Uncertain".

    Example:
        >>> OpcQuality("Good").is_good()
        True
        >>> OpcQuality("Bad").is_good()
        False
    """

    def __init__(self, code):
        """
        Create an OpcQuality from code string.

        Args:
            code: Quality code string (e.g., "Good", "Bad")
        """
        self._code = code

    def text(self):
        """
        Get the quality as lowercase string.

        Returns:
            Lowercase quality string for JSON
        """
        return self._code.lower()

    def is_good(self):
        """
        Check if quality indicates good value.

        Returns:
            True if quality starts with "Good"
        """
        return self._code.lower().startswith("good")

    def __eq__(self, other):
        """
        Check equality with another OpcQuality.

        Args:
            other: Object to compare

        Returns:
            True if other is OpcQuality with same code
        """
        if not isinstance(other, OpcQuality):
            return False
        return self._code.lower() == other._code.lower()

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing OpcQuality and its code
        """
        return "OpcQuality(%r)" % self._code
