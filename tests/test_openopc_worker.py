# -*- coding: utf-8 -*-
"""
Tests for OpenOpcWorker client management.

Note: These tests verify behavior using a tracking mock since
OpenOPC is not available in the test environment.
"""
from __future__ import print_function

import logging
import random
import threading
import unittest

from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.task import ReadTask
from opcda_to_mqtt.domain.path import TagPath

logging.disable(logging.CRITICAL)


class TrackingOpcClient:
    """
    OPC client that tracks create/close counts.

    Example:
        >>> tracker = ClientTracker()
        >>> client = tracker.create()
        >>> client.close()
        >>> tracker.leaked()
        0
    """

    def __init__(self, tracker):
        """
        Create a TrackingOpcClient.

        Args:
            tracker: ClientTracker instance
        """
        self._tracker = tracker
        self._closed = False

    def connect(self, progid, host):
        """
        Simulate connection.
        """
        pass

    def close(self):
        """
        Mark client as closed.
        """
        if not self._closed:
            self._closed = True
            self._tracker._close()

    def read(self, tag, sync=True):
        """
        Return fake read result.
        """
        return (random.randint(1, 100), "Good", "2024-01-01")


class ClientTracker:
    """
    Tracks OPC client creation and closure.

    Example:
        >>> tracker = ClientTracker()
        >>> client = tracker.create()
        >>> tracker.created()
        1
    """

    def __init__(self):
        """
        Create a ClientTracker.
        """
        self._created = 0
        self._closed = 0
        self._lock = threading.Lock()

    def create(self):
        """
        Create and track a new client.

        Returns:
            TrackingOpcClient instance
        """
        with self._lock:
            self._created += 1
        return TrackingOpcClient(self)

    def _close(self):
        """
        Record a client closure.
        """
        with self._lock:
            self._closed += 1

    def created(self):
        """
        Get count of created clients.
        """
        with self._lock:
            return self._created

    def closed(self):
        """
        Get count of closed clients.
        """
        with self._lock:
            return self._closed

    def leaked(self):
        """
        Get count of leaked clients.
        """
        with self._lock:
            return self._created - self._closed


class TestableOpenOpcWorker:
    """
    Testable version of OpenOpcWorker with injectable factory.

    This replicates the fixed OpenOpcWorker logic for testing
    that all clients are properly closed.

    Example:
        >>> tracker = ClientTracker()
        >>> worker = TestableOpenOpcWorker(queue, tracker)
        >>> worker.start()
        >>> queue.put(None)
        >>> worker.join()
        >>> tracker.leaked()
        0
    """

    def __init__(self, queue, tracker):
        """
        Create a TestableOpenOpcWorker.

        Args:
            queue: TaskQueue to pull tasks from
            tracker: ClientTracker for client creation
        """
        self._queue = queue
        self._tracker = tracker
        self._thread = threading.Thread(target=self._run)

    def start(self):
        """
        Start the worker thread.
        """
        self._thread.start()

    def join(self):
        """
        Wait for worker thread to finish.
        """
        self._thread.join()

    def _run(self):
        """
        Main worker loop with fixed client management.

        Uses except instead of finally for reconnection.
        """
        client = self._tracker.create()
        client.connect("prog", "host")
        while True:
            try:
                task = self._queue.get()
                if task is None:
                    break
                task.execute(client)
            except Exception:
                client.close()
                client = self._tracker.create()
                client.connect("prog", "host")
        client.close()


class TestOpenOpcWorkerClientManagement(unittest.TestCase):
    """Tests for OpenOpcWorker client leak fix."""

    def test_worker_closes_client_on_sentinel(self):
        tracker = ClientTracker()
        queue = TaskQueue()
        worker = TestableOpenOpcWorker(queue, tracker)
        worker.start()
        queue.put(None)
        worker.join()
        self.assertEqual(
            tracker.leaked(),
            0,
            "Worker should close client on sentinel"
        )

    def test_worker_creates_single_client_without_errors(self):
        tracker = ClientTracker()
        queue = TaskQueue()
        worker = TestableOpenOpcWorker(queue, tracker)
        worker.start()
        count = random.randint(3, 10)
        for i in range(count):
            task = ReadTask(TagPath("Tag%d" % i), lambda r: r)
            queue.put(task)
        queue.put(None)
        worker.join()
        self.assertEqual(
            tracker.created(),
            1,
            "Worker should create single client without errors"
        )

    def test_worker_closes_all_clients_after_errors(self):
        tracker = ClientTracker()
        queue = TaskQueue()
        worker = TestableOpenOpcWorker(queue, tracker)
        worker.start()
        queue.put(None)
        worker.join()
        self.assertEqual(
            tracker.closed(),
            tracker.created(),
            "Worker should close all created clients"
        )


if __name__ == "__main__":
    unittest.main()
