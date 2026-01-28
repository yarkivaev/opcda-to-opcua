# -*- coding: utf-8 -*-
"""
Node abstraction for OPC address space elements.

Node represents an element in the OPC namespace that can be
readable, writable, or both.

Example usage:
    node = DaReadableNode(path, source)
    result = node.current()
    if result.successful():
        print(result.value().content())
"""
from abc import ABC, abstractmethod


class Node(ABC):
    """
    Interface for OPC namespace element.

    Node represents an addressable element in the OPC server
    namespace, providing access to its path and name.
    """

    @abstractmethod
    def path(self):
        """
        Extract the node's hierarchical path.

        Returns:
            Path: The node's address in the namespace
        """
        pass

    @abstractmethod
    def name(self):
        """
        Extract the node's display name.

        Returns:
            str: The node's human-readable name
        """
        pass


class ReadableNode(Node):
    """
    Interface for readable OPC node.

    ReadableNode extends Node with the ability to retrieve
    current values from the underlying data source.
    """

    @abstractmethod
    def current(self):
        """
        Retrieve current value from data source.

        Returns:
            Either: Right(Reading) on success, Left(Problem) on failure
        """
        pass


class WritableNode(ReadableNode):
    """
    Interface for writable OPC node.

    WritableNode extends ReadableNode with the ability to
    send values to the underlying data source.
    """

    @abstractmethod
    def write(self, value):
        """
        Send value to data source.

        Args:
            value (Value): The value to write

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        pass


class DaNode(Node):
    """
    Basic OPC-DA node without read/write capabilities.

    DaNode represents a namespace element that exists but
    cannot be read or written (e.g., a folder).

    Example usage:
        node = DaNode(path)
        print(node.name())
    """

    def __init__(self, path):
        """
        Create DaNode with path.

        Args:
            path (Path): Node path in namespace
        """
        self._path = path

    def path(self):
        """
        Extract the node's hierarchical path.

        Returns:
            Path: The node's address
        """
        return self._path

    def name(self):
        """
        Extract the node's display name.

        Returns:
            str: The last segment of the path
        """
        return self._path.name()


class DaReadableNode(ReadableNode):
    """
    OPC-DA readable node implementation.

    DaReadableNode can read values from an OPC-DA source.

    Example usage:
        node = DaReadableNode(path, source)
        result = node.current()
    """

    def __init__(self, path, source):
        """
        Create DaReadableNode with path and source.

        Args:
            path (Path): Node path in namespace
            source: DaSource for reading values
        """
        self._path = path
        self._source = source

    def path(self):
        """
        Extract the node's hierarchical path.

        Returns:
            Path: The node's address
        """
        return self._path

    def name(self):
        """
        Extract the node's display name.

        Returns:
            str: The last segment of the path
        """
        return self._path.name()

    def current(self):
        """
        Retrieve current value from OPC-DA source.

        Returns:
            Either: Right(Reading) on success, Left(Problem) on failure
        """
        return self._source.fetch(self._path)


class DaWritableNode(WritableNode):
    """
    OPC-DA writable node implementation.

    DaWritableNode can read and write values via an OPC-DA source.

    Example usage:
        node = DaWritableNode(path, source)
        node.write(TagValue(42, IntVariant()))
    """

    def __init__(self, path, source):
        """
        Create DaWritableNode with path and source.

        Args:
            path (Path): Node path in namespace
            source: DaSource for reading/writing values
        """
        self._path = path
        self._source = source

    def path(self):
        """
        Extract the node's hierarchical path.

        Returns:
            Path: The node's address
        """
        return self._path

    def name(self):
        """
        Extract the node's display name.

        Returns:
            str: The last segment of the path
        """
        return self._path.name()

    def current(self):
        """
        Retrieve current value from OPC-DA source.

        Returns:
            Either: Right(Reading) on success, Left(Problem) on failure
        """
        return self._source.fetch(self._path)

    def write(self, value):
        """
        Send value to OPC-DA source.

        Args:
            value (Value): The value to write

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        return self._source.send(self._path, value)
