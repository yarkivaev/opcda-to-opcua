# -*- coding: utf-8 -*-
"""
OPC-UA target abstraction for server operations.

UaTarget provides the interface to OPC-UA server operations
for mirroring an OPC-DA namespace.

Example usage:
    target = OpcUaTarget(config, server)
    target.start()
    target.mirror(nodes)
    target.subscribe(callback)
"""
from abc import ABC, abstractmethod


class UaTarget(ABC):
    """
    Interface for OPC-UA server target operations.

    UaTarget encapsulates the OPC-UA server that mirrors
    the OPC-DA namespace and handles client interactions.
    """

    @abstractmethod
    def start(self):
        """
        Start the OPC-UA server.

        Returns:
            Either: Right(Running) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Stop the OPC-UA server.

        Returns:
            Either: Right(Stopped) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def mirror(self, nodes):
        """
        Create OPC-UA nodes mirroring OPC-DA namespace.

        Args:
            nodes (list): List of Node objects to mirror

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def update(self, path, reading):
        """
        Update OPC-UA node with new reading.

        Args:
            path (Path): The node path to update
            reading (Reading): The new reading value

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        pass

    @abstractmethod
    def subscribe(self, callback):
        """
        Subscribe to value changes from OPC-UA clients.

        Args:
            callback (Callback): Handler for change notifications

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        pass
