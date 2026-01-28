# -*- coding: utf-8 -*-
"""
OPC-UA server implementation using python-opcua.

OpcUaTarget wraps the python-opcua library to provide an OPC-UA
server that mirrors the OPC-DA namespace.

Note: Requires python-opcua library.

Example usage:
    from opcua import Server
    config = UaConfig("opc.tcp://0.0.0.0:4840")
    server = Server()
    target = OpcUaTarget(config, server)
    target.start()
"""
from opcda_to_opcua.ua.target import UaTarget
from opcda_to_opcua.result.either import Right, Left, Problem
from opcda_to_opcua.domain.markers import Running, Stopped, Success
from opcda_to_opcua.domain.node import WritableNode


class OpcUaTarget(UaTarget):
    """
    python-opcua based implementation of UaTarget.

    OpcUaTarget wraps the python-opcua Server to provide
    OPC-UA server functionality with error handling via Either monad.

    Example usage:
        from opcua import Server
        target = OpcUaTarget(config, Server())
        target.start()
        target.mirror(nodes)
    """

    def __init__(self, config, server):
        """
        Create OpcUaTarget with configuration and server.

        Args:
            config (UaConfig): Server configuration
            server: python-opcua Server instance
        """
        self._config = config
        self._server = server
        self._handles = {}
        self._callback = None

    def start(self):
        """
        Start the OPC-UA server.

        Returns:
            Either: Right(Running) on success, Left(Problem) on failure
        """
        try:
            self._server.set_endpoint(self._config.endpoint())
            self._idx = self._server.register_namespace(self._config.uri())
            self._root = self._server.nodes.objects.add_object(
                self._idx, "OPC-DA Bridge"
            )
            self._server.start()
            return Right(Running())
        except Exception as e:
            return Left(Problem("Server start failed", str(e)))

    def stop(self):
        """
        Stop the OPC-UA server.

        Returns:
            Either: Right(Stopped) on success, Left(Problem) on failure
        """
        try:
            self._server.stop()
            return Right(Stopped())
        except Exception as e:
            return Left(Problem("Server stop failed", str(e)))

    def mirror(self, nodes):
        """
        Create OPC-UA nodes mirroring OPC-DA namespace.

        Args:
            nodes (list): List of Node objects to mirror

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        try:
            folders = {}
            for node in nodes:
                path = node.path()
                segments = path.segments()
                parent = self._root
                for i, seg in enumerate(segments[:-1]):
                    folder_path = '.'.join(segments[:i+1])
                    if folder_path not in folders:
                        folders[folder_path] = parent.add_folder(self._idx, seg)
                    parent = folders[folder_path]
                name = segments[-1] if segments else "Node"
                ua_node = parent.add_variable(self._idx, name, 0)
                if isinstance(node, WritableNode):
                    ua_node.set_writable()
                self._handles[path.text()] = ua_node
            if self._callback:
                self._subscribe()
            return Right(Success())
        except Exception as e:
            return Left(Problem("Mirror failed", str(e)))

    def update(self, path, reading):
        """
        Update OPC-UA node with new reading.

        Args:
            path (Path): The node path to update
            reading (Reading): The new reading value

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        try:
            key = path.text()
            if key in self._handles:
                self._handles[key].set_value(reading.value().content())
            return Right(Success())
        except Exception as e:
            return Left(Problem("Update failed for %s" % path.text(), str(e)))

    def subscribe(self, callback):
        """
        Subscribe to value changes from OPC-UA clients.

        Args:
            callback (Callback): Handler for change notifications

        Returns:
            Either: Right(Success) on success, Left(Problem) on failure
        """
        try:
            self._callback = callback
            if self._handles:
                self._subscribe()
            return Right(Success())
        except Exception as e:
            return Left(Problem("Subscribe failed", str(e)))

    def _subscribe(self):
        """Internal method to set up subscriptions."""
        handler = ChangeHandler(self._callback, self._handles)
        sub = self._server.create_subscription(100, handler)
        writable_handles = []
        for key, handle in self._handles.items():
            writable_handles.append(handle)
        if writable_handles:
            sub.subscribe_data_change(writable_handles)


class ChangeHandler(object):
    """
    Handler for OPC-UA data change notifications.

    ChangeHandler receives notifications when OPC-UA clients
    write values and forwards them to the registered callback.
    """

    def __init__(self, callback, handles):
        """
        Create ChangeHandler with callback and handle mapping.

        Args:
            callback (Callback): Callback to forward writes to
            handles (dict): Map of path text to UA node handles
        """
        self._callback = callback
        self._handles = handles
        self._reverse = {v: k for k, v in handles.items()}
        self._initialized = set()

    def datachange_notification(self, node, val, data):
        """
        Handle data change notification from OPC-UA.

        Note: This is called for initial subscription setup too,
        so we track initialized nodes to skip the first notification.

        Args:
            node: OPC-UA node that changed
            val: New value
            data: Additional data
        """
        node_id = str(node)
        if node_id not in self._initialized:
            self._initialized.add(node_id)
            return
        if self._callback:
            from opcda_to_opcua.domain.path import ParsedPath
            from opcda_to_opcua.domain.value import TagValue
            from opcda_to_opcua.domain.variant import IntVariant, FloatVariant, StringVariant
            for handle, path_text in self._reverse.items():
                if str(handle) == node_id:
                    path = ParsedPath(path_text).path()
                    variant = IntVariant()
                    if isinstance(val, float):
                        variant = FloatVariant()
                    elif isinstance(val, str):
                        variant = StringVariant()
                    value = TagValue(val, variant)
                    self._callback.handle(path, value)
                    break
