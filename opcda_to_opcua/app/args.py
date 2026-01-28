# -*- coding: utf-8 -*-
"""
Command-line argument handling.

Args provides parsing and validation of command-line arguments
for the OPC bridge application.

Example usage:
    args = Args(sys.argv[1:])
    print(args.da_host())
    print(args.ua_endpoint())
"""
import argparse


class Args(object):
    """
    Command-line arguments for the OPC bridge.

    Args parses and provides access to command-line arguments
    with sensible defaults for common use cases.

    Example usage:
        args = Args(["--da-host", "localhost", "--da-progid", "Sim.Server"])
        print(args.da_host())  # localhost
    """

    def __init__(self, argv):
        """
        Parse command-line arguments.

        Args:
            argv (list): Command-line argument list (sys.argv[1:])
        """
        parser = argparse.ArgumentParser(
            description='OPC-DA to OPC-UA Bridge'
        )
        parser.add_argument(
            '--da-host',
            default='localhost',
            help='OPC-DA server hostname'
        )
        parser.add_argument(
            '--da-progid',
            required=True,
            help='OPC-DA server ProgID'
        )
        parser.add_argument(
            '--ua-endpoint',
            default='opc.tcp://0.0.0.0:4840',
            help='OPC-UA server endpoint'
        )
        parser.add_argument(
            '--ua-uri',
            default='http://example.org/opcda-bridge',
            help='OPC-UA namespace URI'
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=500,
            help='Polling interval in milliseconds'
        )
        parser.add_argument(
            '--readonly',
            action='store_true',
            help='Disable write-back to OPC-DA'
        )
        self._args = parser.parse_args(argv)

    def da_host(self):
        """
        Extract OPC-DA hostname.

        Returns:
            str: Hostname or IP address
        """
        return self._args.da_host

    def da_progid(self):
        """
        Extract OPC-DA ProgID.

        Returns:
            str: Server program identifier
        """
        return self._args.da_progid

    def ua_endpoint(self):
        """
        Extract OPC-UA endpoint.

        Returns:
            str: Endpoint URL
        """
        return self._args.ua_endpoint

    def ua_uri(self):
        """
        Extract OPC-UA namespace URI.

        Returns:
            str: Namespace URI
        """
        return self._args.ua_uri

    def interval(self):
        """
        Extract polling interval.

        Returns:
            int: Interval in milliseconds
        """
        return self._args.interval

    def readonly(self):
        """
        Query readonly mode.

        Returns:
            bool: True if readonly mode enabled
        """
        return self._args.readonly
