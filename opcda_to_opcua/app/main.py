# -*- coding: utf-8 -*-
"""
Application entry point for the OPC-DA to OPC-UA bridge.

This module provides the main entry point for running the bridge
as a standalone application.

Example usage:
    python -m opcda_to_opcua.app.main --da-progid "Vendor.OPC.Server"
"""
import sys
import signal
import time

from opcda_to_opcua.app.args import Args
from opcda_to_opcua.app.log import Log
from opcda_to_opcua.domain.config import DaConfig, UaConfig
from opcda_to_opcua.domain.interval import Milliseconds
from opcda_to_opcua.sync.bridge import BridgeSync


def main(argv):
    """
    Main entry point.

    Args:
        argv (list): Command-line arguments (sys.argv[1:])

    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    args = Args(argv)
    logger = Log("opcda_bridge").logger()
    logger.info("Starting OPC-DA to OPC-UA bridge")
    logger.info("DA Host: %s" % args.da_host())
    logger.info("DA ProgID: %s" % args.da_progid())
    logger.info("UA Endpoint: %s" % args.ua_endpoint())
    logger.info("Interval: %d ms" % args.interval())
    logger.info("Readonly: %s" % args.readonly())
    da_config = DaConfig(args.da_host(), args.da_progid())
    ua_config = UaConfig(args.ua_endpoint(), args.ua_uri())
    interval = Milliseconds(args.interval())
    try:
        import OpenOPC
        from opcua import Server
        from opcda_to_opcua.da.openopc import OpenOpcSource
        from opcda_to_opcua.ua.opcua import OpcUaTarget
        source = OpenOpcSource(da_config, OpenOPC.client())
        target = OpcUaTarget(ua_config, Server())
    except ImportError as e:
        logger.error("Missing dependency: %s" % str(e))
        logger.error("Ensure OpenOPC and opcua are installed")
        return 1
    bridge = BridgeSync(source, target, interval, args.readonly())
    running = [True]
    def shutdown(signum, frame):
        """Handle shutdown signal."""
        logger.info("Shutdown signal received")
        running[0] = False
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    result = bridge.start()
    if not result.successful():
        logger.error("Bridge start failed: %s" % result.problem())
        return 1
    logger.info("Bridge running")
    while running[0]:
        time.sleep(0.1)
    logger.info("Stopping bridge")
    result = bridge.stop()
    if not result.successful():
        logger.error("Bridge stop failed: %s" % result.problem())
        return 1
    logger.info("Bridge stopped")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
