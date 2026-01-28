# -*- coding: utf-8 -*-
"""
Path abstraction for OPC node addressing.

Path represents the hierarchical address of an OPC node. It is immutable
and can be converted to text or decomposed into segments.

Example usage:
    path = NodePath(["Simulation", "Random", "Int4"])
    print(path.text())  # Simulation.Random.Int4
    segments = path.segments()  # ["Simulation", "Random", "Int4"]

    parsed = ParsedPath("Simulation.Random.Int4")
    path = parsed.path()
"""
from abc import ABC, abstractmethod
from opcda_to_opcua.result.optional import Some, Empty


class Path(ABC):
    """
    Interface for OPC node path representation.

    Path encapsulates the hierarchical address of an OPC node without
    exposing its internal structure. Implementations must be immutable.
    """

    @abstractmethod
    def segments(self):
        """
        Decompose path into hierarchical segments.

        Returns:
            list: Ordered list of path segment strings
        """
        pass

    @abstractmethod
    def text(self):
        """
        Format path as text string.

        Returns:
            str: Path formatted as dot-separated string
        """
        pass

    @abstractmethod
    def name(self):
        """
        Extract the node name (last segment).

        Returns:
            str: The final segment of the path
        """
        pass

    @abstractmethod
    def parent(self):
        """
        Create path to parent node.

        Returns:
            Optional: Some(Path) if parent exists, Empty otherwise
        """
        pass


class NodePath(Path):
    """
    Immutable path implementation for OPC node addressing.

    NodePath encapsulates a hierarchical path as a tuple of segments
    with a configurable separator for text representation.

    Example usage:
        path = NodePath(["Objects", "Device", "Temperature"])
        print(path.text())  # Objects.Device.Temperature
        print(path.name())  # Temperature
    """

    def __init__(self, segments, separator="."):
        """
        Create NodePath from segments list.

        Args:
            segments (list): Ordered list of path segment strings
            separator (str): Separator for text representation
        """
        self._segments = tuple(segments)
        self._separator = separator

    def segments(self):
        """
        Decompose path into hierarchical segments.

        Returns:
            list: Copy of ordered segment strings
        """
        return list(self._segments)

    def text(self):
        """
        Format path as text string.

        Returns:
            str: Path formatted with configured separator
        """
        return self._separator.join(self._segments)

    def name(self):
        """
        Extract the last segment as the node name.

        Returns:
            str: The final segment, or empty string if no segments
        """
        if self._segments:
            return self._segments[-1]
        return ""

    def parent(self):
        """
        Create path to parent node.

        Returns:
            Optional: Some(NodePath) if parent exists, Empty otherwise
        """
        if len(self._segments) <= 1:
            return Empty()
        return Some(NodePath(self._segments[:-1], self._separator))

    def __eq__(self, other):
        """
        Compare paths for equality.

        Args:
            other: Another path to compare

        Returns:
            bool: True if paths are equal
        """
        if not isinstance(other, NodePath):
            return False
        return self._segments == other._segments

    def __hash__(self):
        """
        Compute hash for use in collections.

        Returns:
            int: Hash based on segments
        """
        return hash(self._segments)


class ParsedPath(object):
    """
    Factory for creating NodePath from text representation.

    ParsedPath parses a text string into a NodePath using
    the specified separator.

    Example usage:
        parsed = ParsedPath("Simulation.Random.Int4")
        path = parsed.path()
        print(path.segments())  # ["Simulation", "Random", "Int4"]
    """

    def __init__(self, text, separator="."):
        """
        Create ParsedPath from text string.

        Args:
            text (str): Path as text string
            separator (str): Separator used in text
        """
        self._text = text
        self._separator = separator

    def path(self):
        """
        Parse text into NodePath.

        Returns:
            NodePath: Parsed path object
        """
        segments = self._text.split(self._separator)
        return NodePath(segments, self._separator)
