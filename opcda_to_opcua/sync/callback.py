# -*- coding: utf-8 -*-
"""
Callback abstraction for write notifications.

Callback provides the interface for handling value changes
from OPC-UA clients.

Example usage:
    class MyCallback(Callback):
        def handle(self, path, value):
            print("Write to %s: %s" % (path.text(), value.content()))
            return Right(Success())
"""
from abc import ABC, abstractmethod


class Callback(ABC):
    """
    Interface for handling write notifications.

    Callback is invoked when an OPC-UA client writes
    a value to a monitored node.
    """

    @abstractmethod
    def handle(self, path, value):
        """
        Handle write request from OPC-UA client.

        Args:
            path (Path): Node path being written
            value (Value): Value being written

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        pass


class LoggingCallback(Callback):
    """
    Callback that logs write operations.

    LoggingCallback records all write operations for debugging
    or auditing purposes, then delegates to another callback.

    Example usage:
        inner = WritebackCallback(source)
        callback = LoggingCallback(inner, logger)
    """

    def __init__(self, delegate, logger):
        """
        Create LoggingCallback with delegate and logger.

        Args:
            delegate (Callback): Callback to forward to
            logger: Logger instance for recording operations
        """
        self._delegate = delegate
        self._logger = logger

    def handle(self, path, value):
        """
        Log and forward write request.

        Args:
            path (Path): Node path being written
            value (Value): Value being written

        Returns:
            Either: Result from delegate
        """
        self._logger.info(
            "Write to %s: %s" % (path.text(), value.content())
        )
        return self._delegate.handle(path, value)
