# -*- coding: utf-8 -*-
"""
Worker interface and FakeWorker implementation.

Example:
    >>> worker = FakeWorker(queue, results)
    >>> worker.start()
    >>> queue.put(task)
    >>> queue.put(None)  # Sentinel
    >>> worker.join()
"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod
import threading


class Worker:
    """
    Interface for task executors.

    Workers pull tasks from a queue and execute them.

    Example:
        >>> class MyWorker(Worker):
        ...     def start(self):
        ...         self._thread.start()
        ...     def stop(self):
        ...         pass  # Bridge sends sentinel
        ...     def join(self):
        ...         self._thread.join()
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self):
        """
        Start the worker thread.
        """
        raise NotImplementedError()

    @abstractmethod
    def stop(self):
        """
        Signal the worker to stop.

        Note: Bridge sends None sentinel to queue.
        """
        raise NotImplementedError()

    @abstractmethod
    def join(self):
        """
        Wait for worker thread to finish.
        """
        raise NotImplementedError()


class FakeWorker(Worker):
    """
    Test double for Worker.

    Executes tasks with a fake client.
    Records all executed tasks.

    Example:
        >>> queue = TaskQueue()
        >>> worker = FakeWorker(queue, {"Tag1": 42})
        >>> worker.start()
        >>> queue.put(ReadTask(TagPath("Tag1"), callback))
        >>> queue.put(None)
        >>> worker.join()
    """

    def __init__(self, queue, readings):
        """
        Create a FakeWorker.

        Args:
            queue: TaskQueue to pull tasks from
            readings: Dict mapping tag paths to values
        """
        self._queue = queue
        self._client = FakeOpcClient(readings)
        self._thread = threading.Thread(target=self._run)
        self._executed = []
        self._lock = threading.Lock()

    def start(self):
        """
        Start the worker thread.
        """
        self._thread.start()

    def stop(self):
        """
        Signal stop (Bridge sends sentinel).
        """
        pass

    def join(self):
        """
        Wait for worker to finish.
        """
        self._thread.join()

    def _run(self):
        """
        Main worker loop.

        Pulls and executes tasks until sentinel.
        """
        while True:
            task = self._queue.get()
            if task is None:
                break
            with self._lock:
                self._executed.append(task)
            task.execute(self._client)

    def executed(self):
        """
        Get list of executed tasks.

        Returns:
            List of Task objects
        """
        with self._lock:
            return list(self._executed)


class FakeOpcClient:
    """
    Fake OPC client for testing.

    Returns predefined values for tag reads.

    Example:
        >>> client = FakeOpcClient({"Tag1": 42})
        >>> client.read("Tag1", sync=True)
        (42, 'Good', ...)
    """

    def __init__(self, readings):
        """
        Create a FakeOpcClient.

        Args:
            readings: Dict mapping tag paths to values
        """
        self._readings = dict(readings)

    def read(self, tag, sync=True):
        """
        Read a tag value.

        Args:
            tag: Tag path string
            sync: Synchronous read flag (ignored)

        Returns:
            Tuple of (value, quality, timestamp)
        """
        value = self._readings.get(tag, 0)
        return (value, "Good", "2024-01-01 00:00:00")

    def connect(self, progid):
        """
        Simulate connection.

        Args:
            progid: OPC server ProgID (ignored)
        """
        pass

    def close(self):
        """
        Simulate disconnection.
        """
        pass
