# -*- coding: utf-8 -*-
"""
Fake OPC-UA target for unit and integration testing.

FakeUaTarget simulates an OPC-UA server without requiring
the actual OPC-UA library, enabling cross-platform testing.

Example usage:
    target = FakeUaTarget()
    target.start()
    target.mirror(nodes)
    target.update(path, reading)
"""
from opcda_to_opcua.ua.target import UaTarget
from opcda_to_opcua.result.either import Right, Left, Problem
from opcda_to_opcua.result.optional import Some, Empty
from opcda_to_opcua.domain.markers import Running, Stopped, Success


class FakeUaTarget(UaTarget):
    """
    Fake implementation of UaTarget for testing.

    FakeUaTarget records operations without running a real
    OPC-UA server, enabling unit tests to verify behavior.

    Example usage:
        target = FakeUaTarget()
        target.start()
        target.mirror(nodes)
    """

    def __init__(self):
        """Create FakeUaTarget in stopped state."""
        self._running = False
        self._mirrored = []
        self._readings = {}
        self._callback = None

    def start(self):
        """
        Simulate server start.

        Returns:
            Either: Right(Running)
        """
        self._running = True
        return Right(Running())

    def stop(self):
        """
        Simulate server stop.

        Returns:
            Either: Right(Stopped)
        """
        self._running = False
        return Right(Stopped())

    def mirror(self, nodes):
        """
        Record mirrored nodes.

        Args:
            nodes (list): List of Node objects to mirror

        Returns:
            Either: Right(Success) or Left(Problem)
        """
        if not self._running:
            return Left(Problem("Server not running", "call start() first"))
        self._mirrored = list(nodes)
        return Right(Success())

    def update(self, path, reading):
        """
        Record updated reading.

        Args:
            path (Path): The node path to update
            reading (Reading): The new reading value

        Returns:
            Either: Right(Success) or Left(Problem)
        """
        if not self._running:
            return Left(Problem("Server not running", "call start() first"))
        self._readings[path.text()] = reading
        return Right(Success())

    def subscribe(self, callback):
        """
        Register callback for write notifications.

        Args:
            callback (Callback): Handler for change notifications

        Returns:
            Either: Right(Success) or Left(Problem)
        """
        if not self._running:
            return Left(Problem("Server not running", "call start() first"))
        self._callback = callback
        return Right(Success())

    def simulate(self, path, value):
        """
        Simulate client write for testing.

        This method is for test setup only, not part
        of the UaTarget interface.

        Args:
            path (Path): The path being written
            value (Value): The value being written
        """
        if self._callback:
            self._callback.handle(path, value)

    def mirrored(self):
        """
        Query mirrored nodes (test helper).

        Returns:
            list: List of mirrored Node objects
        """
        return list(self._mirrored)

    def reading(self, path):
        """
        Query updated reading for path (test helper).

        Args:
            path (Path): The path to query

        Returns:
            Optional: Some(Reading) if updated, Empty otherwise
        """
        key = path.text()
        if key in self._readings:
            return Some(self._readings[key])
        return Empty()
