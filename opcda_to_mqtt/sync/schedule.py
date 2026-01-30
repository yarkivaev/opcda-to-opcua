# -*- coding: utf-8 -*-
"""
Schedule for delayed tag re-enqueueing.

Example:
    >>> schedule = Schedule(timer, Milliseconds(500), queue)
    >>> schedule.later(tag)  # Tag re-enqueued after 500ms
"""
from __future__ import print_function


class Schedule(object):
    """
    Schedules tag re-enqueueing after interval.

    Groups timer, interval, and queue together.
    Three attributes for scheduling concerns.

    Example:
        >>> schedule = Schedule(timer, interval, queue)
        >>> schedule.later(tag)  # Enqueues tag after delay
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

    def later(self, tag):
        """
        Schedule tag re-enqueueing after interval.

        Args:
            tag: Tag to re-enqueue
        """
        self._timer.schedule(self._interval.seconds(), lambda: self._queue.put(tag))

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Schedule configuration
        """
        return "Schedule(%r)" % self._interval
