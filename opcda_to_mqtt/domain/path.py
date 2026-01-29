# -*- coding: utf-8 -*-
"""
TagPath domain object representing an OPC tag path.

Example:
    >>> tag = TagPath("COM1.Device.Temperature")
    >>> tag.text()
    'COM1.Device.Temperature'
"""
from __future__ import print_function


class TagPath:
    """
    Immutable OPC tag path.

    Represents a hierarchical path to an OPC tag.
    The path is a dot-separated string.

    Example:
        >>> tag = TagPath("COM1.Device.Sensor")
        >>> tag.text()
        'COM1.Device.Sensor'
        >>> tag.topic("factory")
        'factory/COM1.Device.Sensor'
    """

    def __init__(self, path):
        """
        Create a TagPath from string.

        Args:
            path: Dot-separated OPC tag path string

        Raises:
            ValueError: If path is empty
        """
        if not path:
            raise ValueError("Tag path cannot be empty")
        self._path = path

    def text(self):
        """
        Get the path as string.

        Returns:
            The tag path string
        """
        return self._path

    def topic(self, prefix):
        """
        Convert to MQTT topic with prefix.

        Args:
            prefix: Base topic prefix

        Returns:
            MQTT topic string as prefix/path
        """
        return "%s/%s" % (prefix, self._path)

    def __eq__(self, other):
        """
        Check equality with another TagPath.

        Args:
            other: Object to compare

        Returns:
            True if other is TagPath with same path
        """
        if not isinstance(other, TagPath):
            return False
        return self._path == other._path

    def __hash__(self):
        """
        Get hash code for use in sets and dicts.

        Returns:
            Hash of the path string
        """
        return hash(self._path)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing TagPath and its value
        """
        return "TagPath(%r)" % self._path
