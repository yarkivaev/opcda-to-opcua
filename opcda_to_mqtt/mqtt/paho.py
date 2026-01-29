# -*- coding: utf-8 -*-
"""
PahoBroker for real MQTT publishing.

Example:
    >>> broker = PahoBroker("192.168.1.100", 1883)
    >>> broker.connect()
    >>> broker.publish("topic", "message")
    >>> broker.disconnect()
"""
from __future__ import print_function

from opcda_to_mqtt.mqtt.broker import (
    MqttBroker, Connected, Published, Disconnected
)
from opcda_to_mqtt.result.either import Right, Left, Problem


class PahoBroker(MqttBroker):
    """
    Real MQTT broker using paho-mqtt.

    Connects to MQTT broker and publishes messages.

    Example:
        >>> broker = PahoBroker("localhost", 1883)
        >>> broker.connect().is_right()
        True
    """

    def __init__(self, host, port):
        """
        Create a PahoBroker.

        Args:
            host: MQTT broker hostname
            port: MQTT broker port
        """
        self._host = host
        self._port = port
        self._client = None

    def connect(self):
        """
        Connect to the MQTT broker.

        Returns:
            Either[Problem, Connected]
        """
        try:
            import paho.mqtt.client as mqtt
            self._client = mqtt.Client()
            self._client.connect(self._host, self._port)
            self._client.loop_start()
            return Right(Connected())
        except Exception as e:
            return Left(Problem(
                "MQTT connection failed",
                {"host": self._host, "port": str(self._port), "error": str(e)}
            ))

    def publish(self, topic, message):
        """
        Publish a message to a topic.

        Args:
            topic: MQTT topic string
            message: Message content string

        Returns:
            Either[Problem, Published]
        """
        try:
            if self._client is None:
                return Left(Problem("Not connected", {}))
            self._client.publish(topic, message)
            return Right(Published())
        except Exception as e:
            return Left(Problem(
                "MQTT publish failed",
                {"topic": topic, "error": str(e)}
            ))

    def disconnect(self):
        """
        Disconnect from the MQTT broker.

        Returns:
            Either[Problem, Disconnected]
        """
        try:
            if self._client is not None:
                self._client.loop_stop()
                self._client.disconnect()
                self._client = None
            return Right(Disconnected())
        except Exception as e:
            return Left(Problem(
                "MQTT disconnect failed",
                {"error": str(e)}
            ))

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing PahoBroker configuration
        """
        return "PahoBroker(%r, %d)" % (self._host, self._port)
