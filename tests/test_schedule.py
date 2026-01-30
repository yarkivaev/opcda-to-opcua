# -*- coding: utf-8 -*-
"""
Tests for Schedule.
"""
from __future__ import print_function

import logging
import random
import time
import unittest

from opcda_to_mqtt.sync.schedule import Schedule
from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.timer import TimerThread
from opcda_to_mqtt.domain.interval import Milliseconds

logging.disable(logging.CRITICAL)


class TestSchedule(unittest.TestCase):
    """Tests for Schedule."""

    def test_schedule_fires_callback_after_interval(self):
        timer = TimerThread()
        queue = TaskQueue()
        interval = Milliseconds(random.randint(10, 30))
        schedule = Schedule(timer, interval, queue)
        results = []
        timer.start()
        schedule.later(lambda: results.append(1))
        time.sleep(0.1)
        timer.stop()
        self.assertEqual(
            len(results),
            1,
            "Schedule should fire callback after interval"
        )

    def test_schedule_enqueue_puts_tag_in_queue(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        marker = object()
        schedule.enqueue(marker)
        self.assertEqual(
            queue.size(),
            1,
            "Schedule enqueue should put tag in queue"
        )

    def test_schedule_enqueue_preserves_identity(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        marker = object()
        schedule.enqueue(marker)
        result = queue.get()
        self.assertIs(
            result,
            marker,
            "Schedule enqueue should preserve tag identity"
        )

    def test_schedule_uses_configured_interval(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        results = []
        timer.start()
        schedule.later(lambda: results.append(1))
        time.sleep(0.02)
        early = len(results)
        time.sleep(0.15)
        timer.stop()
        self.assertEqual(
            early,
            0,
            "Schedule should wait for interval before firing"
        )

    def test_schedule_repr_shows_interval(self):
        timer = TimerThread()
        queue = TaskQueue()
        amount = random.randint(100, 999)
        schedule = Schedule(timer, Milliseconds(amount), queue)
        self.assertIn(
            str(amount),
            repr(schedule),
            "Schedule repr should show interval"
        )

    def test_schedule_handles_multiple_callbacks(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(random.randint(5, 15)), queue)
        count = random.randint(3, 7)
        results = []
        timer.start()
        for i in range(count):
            schedule.later(lambda i=i: results.append(i))
        time.sleep(0.1)
        timer.stop()
        self.assertEqual(
            len(results),
            count,
            "Schedule should handle multiple callbacks"
        )


if __name__ == "__main__":
    unittest.main()
