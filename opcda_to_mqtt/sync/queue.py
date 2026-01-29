# -*- coding: utf-8 -*-
"""
TaskQueue for thread-safe task distribution.

Example:
    >>> queue = TaskQueue()
    >>> queue.put(task)
    >>> task = queue.get()
"""
from __future__ import print_function

import Queue as queue_module


class TaskQueue:
    """
    Thread-safe FIFO queue for tasks.

    Workers pull tasks from this queue for execution.

    Example:
        >>> q = TaskQueue()
        >>> q.put(task1)
        >>> q.put(task2)
        >>> q.get()  # Returns task1
        >>> q.get()  # Returns task2
    """

    def __init__(self):
        """
        Create an empty TaskQueue.
        """
        self._queue = queue_module.Queue()

    def put(self, task):
        """
        Add a task to the queue.

        Args:
            task: Task to add (or None for shutdown sentinel)
        """
        self._queue.put(task)

    def get(self):
        """
        Remove and return the next task.

        Blocks until a task is available.

        Returns:
            Next task from queue (or None sentinel)
        """
        return self._queue.get()

    def size(self):
        """
        Get approximate queue size.

        Returns:
            Number of tasks in queue
        """
        return self._queue.qsize()

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing TaskQueue and its size
        """
        return "TaskQueue(size=%d)" % self.size()
