# -*- coding: utf-8 -*-
"""
Configuration objects for OPC connections.

Example usage:
    da_config = DaConfig("localhost", "Vendor.OPC.Server")
    ua_config = UaConfig("opc.tcp://0.0.0.0:4840")
"""


class DaConfig(object):
    """
    Configuration for OPC-DA connection.

    DaConfig encapsulates the parameters needed to connect
    to an OPC-DA server.

    Example usage:
        config = DaConfig("192.168.1.100", "Vendor.OPC.Server")
        print(config.host())  # 192.168.1.100
        print(config.progid())  # Vendor.OPC.Server
    """

    def __init__(self, host, progid):
        """
        Create DaConfig with connection parameters.

        Args:
            host (str): OPC server hostname or IP
            progid (str): OPC server ProgID
        """
        self._host = host
        self._progid = progid

    def host(self):
        """
        Extract the server hostname.

        Returns:
            str: Hostname or IP address
        """
        return self._host

    def progid(self):
        """
        Extract the server ProgID.

        Returns:
            str: OPC server program identifier
        """
        return self._progid


class UaConfig(object):
    """
    Configuration for OPC-UA server.

    UaConfig encapsulates the parameters needed to run
    an OPC-UA server.

    Example usage:
        config = UaConfig("opc.tcp://0.0.0.0:4840", "urn:example:server")
        print(config.endpoint())  # opc.tcp://0.0.0.0:4840
    """

    def __init__(self, endpoint, uri="http://example.org"):
        """
        Create UaConfig with server parameters.

        Args:
            endpoint (str): OPC-UA server endpoint URL
            uri (str): Server namespace URI
        """
        self._endpoint = endpoint
        self._uri = uri

    def endpoint(self):
        """
        Extract the server endpoint URL.

        Returns:
            str: OPC-UA endpoint URL
        """
        return self._endpoint

    def uri(self):
        """
        Extract the namespace URI.

        Returns:
            str: Server namespace URI
        """
        return self._uri
