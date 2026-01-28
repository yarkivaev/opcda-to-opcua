# -*- coding: utf-8 -*-
"""
OPC-DA to OPC-UA Bridge Library.

This library provides a production-ready bridge between OPC-DA (Classic)
and OPC-UA servers, enabling legacy OPC-DA systems to be accessed via
the modern OPC-UA protocol.

Example usage:
    from opcda_to_opcua.da.openopc import OpenOpcSource
    from opcda_to_opcua.ua.opcua import OpcUaTarget
    from opcda_to_opcua.sync.bridge import BridgeSync
    from opcda_to_opcua.domain.config import DaConfig, UaConfig
    from opcda_to_opcua.domain.interval import Milliseconds

    da_config = DaConfig("localhost", "Vendor.OPC.Server")
    ua_config = UaConfig("opc.tcp://0.0.0.0:4840")

    source = OpenOpcSource(da_config)
    target = OpcUaTarget(ua_config)
    bridge = BridgeSync(source, target, Milliseconds(500))

    result = bridge.start()
    if result.successful():
        print("Bridge running")
"""
