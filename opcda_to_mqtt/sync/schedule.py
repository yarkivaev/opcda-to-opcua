# -*- coding: utf-8 -*-
"""
Schedule for delayed callback execution.

Example:
    >>> schedule = Schedule(timer, Milliseconds(500), queue)
    >>> schedule.later(callback)  # Callback fires after 500ms
    >>> schedule.enqueue(tag)  # Tag added to queue immediately
"""
from __future__ import print_function


class Schedule(object):
    """
    Schedules callbacks after interval.

    Groups timer, interval, and queue together.
    Three attributes for scheduling concerns.

    Example:
        >>> schedule = Schedule(timer, interval, queue)
        >>> schedule.later(callback)  # Fires callback after delay
    """

    def __init__(self, timer, interval, queue):
        """
        Create a Schedule.

        Args:
            timer: TimerThread for delayed execution
            interval: Milliseconds between reads
            queue: TaskQueue for tag submission
        """
        self._timer = timer
        self._interval = interval
        self._queue = queue

    def later(self, callback):
        """
        Schedule callback after interval.

        Args:
            callback: Function to call after delay
        """
        self._timer.schedule(self._interval.seconds(), callback)

    def enqueue(self, tag):
        """
        Put tag in queue immediately.

        Args:
            tag: Tag to enqueue
        """
        self._queue.put(tag)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Schedule configuration
        """
        return "Schedule(%r)" % self._interval
