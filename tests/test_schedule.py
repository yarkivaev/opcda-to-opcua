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

    def test_schedule_enqueues_tag_after_interval(self):
        timer = TimerThread()
        queue = TaskQueue()
        interval = Milliseconds(random.randint(10, 30))
        schedule = Schedule(timer, interval, queue)
        marker = object()
        timer.start()
        schedule.later(marker)
        time.sleep(0.1)
        timer.stop()
        self.assertEqual(
            queue.size(),
            1,
            "Schedule should enqueue tag after interval"
        )

    def test_schedule_preserves_tag_identity(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(random.randint(5, 15)), queue)
        marker = object()
        timer.start()
        schedule.later(marker)
        time.sleep(0.1)
        timer.stop()
        result = queue.get()
        self.assertIs(
            result,
            marker,
            "Schedule should preserve tag identity"
        )

    def test_schedule_uses_configured_interval(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(100), queue)
        marker = object()
        timer.start()
        schedule.later(marker)
        time.sleep(0.02)
        early = queue.size()
        time.sleep(0.15)
        timer.stop()
        self.assertEqual(
            early,
            0,
            "Schedule should wait for interval before enqueueing"
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

    def test_schedule_handles_multiple_tags(self):
        timer = TimerThread()
        queue = TaskQueue()
        schedule = Schedule(timer, Milliseconds(random.randint(5, 15)), queue)
        count = random.randint(3, 7)
        markers = [object() for _ in range(count)]
        timer.start()
        for marker in markers:
            schedule.later(marker)
        time.sleep(0.1)
        timer.stop()
        self.assertEqual(
            queue.size(),
            count,
            "Schedule should handle multiple tags"
        )


if __name__ == "__main__":
    unittest.main()
