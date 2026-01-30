# -*- coding: utf-8 -*-
"""
Bridge orchestrator for OPC-DA to MQTT publishing.

Example:
    >>> bridge = Bridge(queue, workers, timer, broker)
    >>> bridge.start(paths, interval, topic)  # Starts polling
    >>> bridge.stop()  # Stops gracefully
"""
from __future__ import print_function

from opcda_to_mqtt.domain.tag import Tag
from opcda_to_mqtt.sync.schedule import Schedule


class Bridge:
    """
    Orchestrates OPC-DA reading and MQTT publishing.

    Manages workers, timer, and task flow.

    Example:
        >>> bridge = Bridge(queue, workers, timer, broker)
        >>> bridge.start([TagPath("Tag1"), TagPath("Tag2")], interval, topic)
        >>> # Tags are continuously read and published
        >>> bridge.stop()
    """

    def __init__(self, queue, workers, timer, broker):
        """
        Create a Bridge.

        Args:
            queue: TaskQueue for task distribution
            workers: List of Worker instances
            timer: TimerThread for delayed scheduling
            broker: MqttBroker for publishing
        """
        self._queue = queue
        self._workers = workers
        self._timer = timer
        self._broker = broker

    def start(self, paths, interval, topic):
        """
        Start the bridge with given tag paths.

        Args:
            paths: List of TagPath to monitor
            interval: Milliseconds between reads
            topic: Base MQTT topic prefix
        """
        schedule = Schedule(self._timer, interval, self._queue)
        self._broker.connect()
        self._timer.start()
        for worker in self._workers:
            worker.start()
        for path in paths:
            tag = Tag(path, self._broker, topic, schedule)
            self._queue.put(tag)

    def stop(self):
        """
        Stop the bridge.

        Stops timer, sends sentinels, waits for workers.
        """
        self._timer.stop()
        for _ in self._workers:
            self._queue.put(None)
        for worker in self._workers:
            worker.join()
        self._broker.disconnect()

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Bridge configuration
        """
        return "Bridge(workers=%d)" % len(self._workers)
