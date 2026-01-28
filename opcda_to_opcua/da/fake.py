# -*- coding: utf-8 -*-
"""
Fake OPC-DA source for unit and integration testing.

FakeDaSource simulates an OPC-DA server without requiring
Windows COM, enabling cross-platform testing.

Example usage:
    paths = [NodePath(["Sim", "Int1"]), NodePath(["Sim", "Real1"])]
    values = {
        "Sim.Int1": TagValue(42, IntVariant()),
        "Sim.Real1": TagValue(3.14, FloatVariant())
    }
    source = FakeDaSource(paths, values)
    source.connect()
    result = source.fetch(paths[0])
"""
from opcda_to_opcua.da.source import DaSource
from opcda_to_opcua.result.either import Right, Left, Problem
from opcda_to_opcua.result.optional import Some, Empty
from opcda_to_opcua.domain.markers import Connected, Disconnected, Success
from opcda_to_opcua.domain.reading import OpcReading, TimestampNow
from opcda_to_opcua.domain.quality import OpcQuality
from opcda_to_opcua.domain.node import DaReadableNode, DaWritableNode


class FakeDaSource(DaSource):
    """
    Fake implementation of DaSource for testing.

    FakeDaSource provides configurable responses without
    requiring actual OPC-DA server connection, enabling
    unit tests to run on any platform.

    Example usage:
        source = FakeDaSource(paths, values)
        source.connect()
        reading = source.fetch(path).value()
    """

    def __init__(self, paths, values, writable=None):
        """
        Create FakeDaSource with predefined data.

        Args:
            paths (list): List of Path objects in namespace
            values (dict): Map of path text to Value objects
            writable (set): Set of path texts that are writable
        """
        self._paths = paths
        self._values = dict(values)
        self._writable = writable if writable else set()
        self._connected = False
        self._written = {}

    def connect(self):
        """
        Simulate successful connection.

        Returns:
            Either: Right(Connected)
        """
        self._connected = True
        return Right(Connected())

    def disconnect(self):
        """
        Simulate successful disconnection.

        Returns:
            Either: Right(Disconnected)
        """
        self._connected = False
        return Right(Disconnected())

    def discover(self):
        """
        Return predefined nodes.

        Returns:
            Either: Right(list of Node) or Left(Problem) if not connected
        """
        if not self._connected:
            return Left(Problem("Not connected", "call connect() first"))
        nodes = []
        for path in self._paths:
            if path.text() in self._writable:
                nodes.append(DaWritableNode(path, self))
            else:
                nodes.append(DaReadableNode(path, self))
        return Right(nodes)

    def fetch(self, path):
        """
        Return predefined value for path.

        Args:
            path (Path): The node path to read

        Returns:
            Either: Right(Reading) or Left(Problem)
        """
        if not self._connected:
            return Left(Problem("Not connected", "call connect() first"))
        key = path.text()
        if key in self._values:
            value = self._values[key]
            quality = OpcQuality(192)
            timestamp = TimestampNow()
            return Right(OpcReading(path, value, quality, timestamp))
        return Left(Problem("Item not found", key))

    def send(self, path, value):
        """
        Record write and return success.

        Args:
            path (Path): The node path to write
            value (Value): The value to write

        Returns:
            Either: Right(Success) or Left(Problem)
        """
        if not self._connected:
            return Left(Problem("Not connected", "call connect() first"))
        key = path.text()
        if key not in self._writable and self._writable:
            return Left(Problem("Item not writable", key))
        self._written[key] = value
        self._values[key] = value
        return Right(Success())

    def written(self, path):
        """
        Query what was written to path (test helper).

        This method is for test verification only, not part
        of the DaSource interface.

        Args:
            path (Path): The path to query

        Returns:
            Optional: Some(Value) if written, Empty otherwise
        """
        key = path.text()
        if key in self._written:
            return Some(self._written[key])
        return Empty()

    def inject(self, path, value):
        """
        Inject a value for testing (test helper).

        This method is for test setup only, not part
        of the DaSource interface.

        Args:
            path (Path): The path to inject
            value (Value): The value to inject
        """
        self._values[path.text()] = value
