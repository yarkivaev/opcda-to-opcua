# -*- coding: utf-8 -*-
"""
OpenOPC-based OPC-DA source implementation.

OpenOpcSource wraps the OpenOPC library to provide OPC-DA
access following Elegant Objects principles.

Note: This implementation requires Windows and OpenOPC library.

Example usage:
    import OpenOPC
    config = DaConfig("localhost", "Vendor.OPC.Server")
    client = OpenOPC.client()
    source = OpenOpcSource(config, client)
    result = source.connect()
"""
from opcda_to_opcua.da.source import DaSource
from opcda_to_opcua.result.either import Right, Left, Problem
from opcda_to_opcua.domain.markers import Connected, Disconnected, Success
from opcda_to_opcua.domain.path import NodePath
from opcda_to_opcua.domain.value import TagValue
from opcda_to_opcua.domain.quality import OpcQuality
from opcda_to_opcua.domain.reading import OpcReading, Timestamp
from opcda_to_opcua.domain.variant import (
    IntVariant, Uint16Variant, FloatVariant, DoubleVariant,
    StringVariant, BoolVariant
)
from opcda_to_opcua.domain.node import DaReadableNode, DaWritableNode, DaNode
import decimal
import time


class OpenOpcSource(DaSource):
    """
    OpenOPC-based implementation of DaSource.

    OpenOpcSource wraps the OpenOPC library to provide OPC-DA
    server access with error handling via Either monad.

    Example usage:
        import OpenOPC
        source = OpenOpcSource(config, OpenOPC.client())
        result = source.connect()
        if result.successful():
            nodes = source.discover()
    """

    def __init__(self, config, client):
        """
        Create OpenOpcSource with configuration and client.

        Args:
            config (DaConfig): Connection configuration
            client: OpenOPC client instance
        """
        self._config = config
        self._client = client

    def connect(self):
        """
        Establish connection to OPC-DA server.

        Returns:
            Either: Right(Connected) on success, Left(Problem) on failure
        """
        try:
            self._client.connect(
                self._config.progid(),
                self._config.host()
            )
            return Right(Connected())
        except Exception as e:
            return Left(Problem("Connection failed", str(e)))

    def disconnect(self):
        """
        Terminate connection to OPC-DA server.

        Returns:
            Either: Right(Disconnected) on success, Left(Problem) on failure
        """
        try:
            self._client.close()
            return Right(Disconnected())
        except Exception as e:
            return Left(Problem("Disconnect failed", str(e)))

    def discover(self):
        """
        Enumerate all nodes in server namespace.

        Returns:
            Either: Right(list of Node) on success, Left(Problem) on failure
        """
        try:
            items = self._client.list('*', recursive=True)
            nodes = []
            for item in items:
                path = NodePath(item.split('.'))
                node = self._classify(path)
                nodes.append(node)
            return Right(nodes)
        except Exception as e:
            return Left(Problem("Discovery failed", str(e)))

    def _classify(self, path):
        """
        Classify node as readable, writable, or neither.

        Args:
            path (NodePath): Node path

        Returns:
            Node: Appropriate node type
        """
        try:
            props = self._client.properties(path.text())
            readable = False
            writable = False
            for prop in props:
                if prop[0] == 5:  # Access Rights
                    value = prop[2]
                    if isinstance(value, str):
                        readable = 'Read' in value
                        writable = 'Write' in value
                    else:
                        readable = (value & 1) != 0
                        writable = (value & 2) != 0
            if writable:
                return DaWritableNode(path, self)
            if readable:
                return DaReadableNode(path, self)
            return DaNode(path)
        except Exception:
            return DaNode(path)

    def fetch(self, path):
        """
        Read current value from specified path.

        Args:
            path (Path): The node path to read

        Returns:
            Either: Right(Reading) on success, Left(Problem) on failure
        """
        try:
            result = self._client.read(path.text())
            value = self._extract(result[0])
            quality = OpcQuality(self._quality(result[1]))
            timestamp = Timestamp(self._timestamp(result[2]))
            return Right(OpcReading(path, value, quality, timestamp))
        except Exception as e:
            return Left(Problem("Read failed for %s" % path.text(), str(e)))

    def _extract(self, raw):
        """
        Extract and convert value from OPC-DA response.

        Args:
            raw: Raw value from OpenOPC

        Returns:
            TagValue: Converted value with variant
        """
        content = raw
        if isinstance(raw, decimal.Decimal):
            content = float(raw)
            return TagValue(content, DoubleVariant())
        if isinstance(raw, float):
            return TagValue(raw, FloatVariant())
        if isinstance(raw, bool):
            return TagValue(raw, BoolVariant())
        if isinstance(raw, int):
            return TagValue(raw, IntVariant())
        if isinstance(raw, str):
            return TagValue(raw, StringVariant())
        return TagValue(content, IntVariant())

    def _quality(self, raw):
        """
        Extract quality code from OPC-DA response.

        Args:
            raw: Raw quality from OpenOPC

        Returns:
            int: Quality code
        """
        if isinstance(raw, str):
            if 'Good' in raw:
                return 192
            if 'Bad' in raw:
                return 0
            return 64
        return int(raw) if raw else 192

    def _timestamp(self, raw):
        """
        Extract timestamp from OPC-DA response.

        Args:
            raw: Raw timestamp from OpenOPC

        Returns:
            float: Epoch seconds
        """
        if raw:
            try:
                return time.mktime(raw.timetuple())
            except Exception:
                pass
        return time.time()

    def send(self, path, value):
        """
        Write value to specified path.

        Args:
            path (Path): The node path to write
            value (Value): The value to write

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        try:
            self._client.write((path.text(), value.content()))
            return Right(Success())
        except Exception as e:
            return Left(Problem("Write failed for %s" % path.text(), str(e)))
