# -*- coding: utf-8 -*-
"""
Bridge synchronization for OPC-DA to OPC-UA.

BridgeSync coordinates continuous bidirectional synchronization
between an OPC-DA source and an OPC-UA target.

Example usage:
    bridge = BridgeSync(source, target, Milliseconds(500))
    result = bridge.start()
    if result.successful():
        print("Bridge running")
    # Later...
    bridge.stop()
"""
import threading
import time

from opcda_to_opcua.result.either import Right, Left, Problem
from opcda_to_opcua.domain.markers import Running, Stopped
from opcda_to_opcua.domain.node import ReadableNode


class BridgeSync(object):
    """
    Bidirectional synchronization between OPC-DA and OPC-UA.

    BridgeSync polls OPC-DA source at configured interval and
    updates OPC-UA target. It also subscribes to OPC-UA changes
    and writes them back to OPC-DA.

    Example usage:
        bridge = BridgeSync(source, target, Milliseconds(500))
        bridge.start()
        # Bridge runs in background
        bridge.stop()
    """

    def __init__(self, source, target, interval, readonly=False):
        """
        Create BridgeSync with source, target, and interval.

        Args:
            source (DaSource): OPC-DA data source
            target (UaTarget): OPC-UA server target
            interval (Interval): Polling interval
            readonly (bool): If True, disable write-back to OPC-DA
        """
        self._source = source
        self._target = target
        self._interval = interval
        self._readonly = readonly

    def start(self):
        """
        Begin synchronization.

        This method:
        1. Connects to OPC-DA source
        2. Discovers OPC-DA namespace
        3. Starts OPC-UA server
        4. Mirrors namespace to OPC-UA
        5. Subscribes to OPC-UA writes (if not readonly)
        6. Starts polling thread

        Returns:
            Either: Right(Running) on success, Left(Problem) on failure
        """
        connect = self._source.connect()
        if not connect.successful():
            return Left(Problem("Source connection failed", str(connect.problem())))
        discovery = self._source.discover()
        if not discovery.successful():
            return Left(Problem("Discovery failed", str(discovery.problem())))
        self._nodes = discovery.value()
        start = self._target.start()
        if not start.successful():
            return Left(Problem("Target start failed", str(start.problem())))
        mirror = self._target.mirror(self._nodes)
        if not mirror.successful():
            return Left(Problem("Mirror failed", str(mirror.problem())))
        if not self._readonly:
            callback = WritebackCallback(self._source)
            subscribe = self._target.subscribe(callback)
            if not subscribe.successful():
                return Left(Problem("Subscribe failed", str(subscribe.problem())))
        self._running = True
        self._thread = threading.Thread(target=self._loop)
        self._thread.daemon = True
        self._thread.start()
        return Right(Running())

    def stop(self):
        """
        Terminate synchronization.

        Returns:
            Either: Right(Stopped) on success, Left(Problem) on failure
        """
        self._running = False
        if hasattr(self, '_thread') and self._thread:
            self._thread.join(timeout=self._interval.seconds() * 2)
        stop = self._target.stop()
        if not stop.successful():
            return Left(Problem("Target stop failed", str(stop.problem())))
        disconnect = self._source.disconnect()
        if not disconnect.successful():
            return Left(Problem("Source disconnect failed", str(disconnect.problem())))
        return Right(Stopped())

    def _loop(self):
        """Internal polling loop."""
        while self._running:
            self._poll()
            time.sleep(self._interval.seconds())

    def _poll(self):
        """Poll all readable nodes and update target."""
        for node in self._nodes:
            if isinstance(node, ReadableNode):
                result = node.current()
                if result.successful():
                    self._target.update(node.path(), result.value())


class WritebackCallback(object):
    """
    Callback for handling OPC-UA write requests.

    WritebackCallback forwards write requests from OPC-UA
    clients back to the OPC-DA source.

    Example usage:
        callback = WritebackCallback(source)
        target.subscribe(callback)
    """

    def __init__(self, source):
        """
        Create callback with source reference.

        Args:
            source (DaSource): Source to write back to
        """
        self._source = source

    def handle(self, path, value):
        """
        Handle write request from OPC-UA client.

        Args:
            path (Path): Node path being written
            value (Value): Value to write

        Returns:
            Either: Result of write operation
        """
        return self._source.send(path, value)
