# -*- coding: utf-8 -*-
"""
TagValue domain object representing a tag's value.

Example:
    >>> value = TagValue(42.5)
    >>> value.content()
    42.5
"""
from __future__ import print_function


class TagValue:
    """
    Immutable tag value wrapper.

    Wraps any value read from an OPC tag.
    Supports integers, floats, strings, booleans.

    Example:
        >>> TagValue(123).content()
        123
        >>> TagValue("hello").content()
        'hello'
    """

    def __init__(self, content):
        """
        Create a TagValue wrapping the given content.

        Args:
            content: The value to wrap (any type)
        """
        self._content = content

    def content(self):
        """
        Get the wrapped value.

        Returns:
            The contained value
        """
        return self._content

    def json(self):
        """
        Convert to JSON-compatible representation.

        Returns:
            The value in JSON-compatible form
        """
        return self._content

    def __eq__(self, other):
        """
        Check equality with another TagValue.

        Args:
            other: Object to compare

        Returns:
            True if other is TagValue with same content
        """
        if not isinstance(other, TagValue):
            return False
        return self._content == other._content

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing TagValue and its content
        """
        return "TagValue(%r)" % self._content
