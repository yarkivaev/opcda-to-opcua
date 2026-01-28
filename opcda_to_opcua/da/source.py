# -*- coding: utf-8 -*-
"""
OPC-DA source abstraction for data access operations.

DaSource provides the interface to OPC-DA server operations
without exposing the underlying COM/DCOM implementation.

Example usage:
    source = OpenOpcSource(config, client)
    result = source.connect()
    if result.successful():
        nodes = source.discover()
"""
from abc import ABC, abstractmethod


class DaSource(ABC):
    """
    Interface for OPC-DA data source operations.

    DaSource encapsulates connection to and operations on an
    OPC-DA server, enabling different implementations for
    production and testing.
    """

    @abstractmethod
    def connect(self):
        """
        Establish connection to OPC-DA server.

        Returns:
            Either: Right(Connected) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def disconnect(self):
        """
        Terminate connection to OPC-DA server.

        Returns:
            Either: Right(Disconnected) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def discover(self):
        """
        Enumerate all nodes in server namespace.

        Returns:
            Either: Right(list of Node) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def fetch(self, path):
        """
        Read current value from specified path.

        Args:
            path (Path): The node path to read

        Returns:
            Either: Right(Reading) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def send(self, path, value):
        """
        Write value to specified path.

        Args:
            path (Path): The node path to write
            value (Value): The value to write

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        pass
