# -*- coding: utf-8 -*-
"""
Tests for TimerThread.
"""
from __future__ import print_function

import logging
import random
import threading
import time
import unittest

from opcda_to_mqtt.sync.timer import TimerThread

logging.disable(logging.CRITICAL)


class TestTimerThread(unittest.TestCase):
    """Tests for TimerThread."""

    def test_timer_starts_with_no_pending(self):
        timer = TimerThread()
        self.assertEqual(
            timer.pending(),
            0,
            "TimerThread should start with no pending"
        )

    def test_timer_schedule_increases_pending(self):
        timer = TimerThread()
        timer.start()
        try:
            timer.schedule(10.0, lambda: 1)
            self.assertEqual(
                timer.pending(),
                1,
                "TimerThread.schedule should increase pending"
            )
        finally:
            timer.stop()

    def test_timer_fires_callback_after_delay(self):
        timer = TimerThread()
        timer.start()
        fired = []
        try:
            timer.schedule(0.01, lambda: fired.append(1))
            time.sleep(0.05)
            self.assertEqual(
                len(fired),
                1,
                "TimerThread should fire callback after delay"
            )
        finally:
            timer.stop()

    def test_timer_fires_multiple_callbacks(self):
        timer = TimerThread()
        timer.start()
        fired = []
        try:
            count = random.randint(3, 7)
            for i in range(count):
                timer.schedule(0.01, lambda n=i: fired.append(n))
            time.sleep(0.1)
            self.assertEqual(
                len(fired),
                count,
                "TimerThread should fire multiple callbacks"
            )
        finally:
            timer.stop()

    def test_timer_fires_in_order_by_time(self):
        timer = TimerThread()
        timer.start()
        fired = []
        try:
            timer.schedule(0.03, lambda: fired.append(3))
            timer.schedule(0.01, lambda: fired.append(1))
            timer.schedule(0.02, lambda: fired.append(2))
            time.sleep(0.1)
            self.assertEqual(
                fired,
                [1, 2, 3],
                "TimerThread should fire in order by time"
            )
        finally:
            timer.stop()

    def test_timer_stop_prevents_pending_fires(self):
        timer = TimerThread()
        timer.start()
        fired = []
        timer.schedule(1.0, lambda: fired.append(1))
        timer.stop()
        self.assertEqual(
            len(fired),
            0,
            "TimerThread.stop should prevent pending fires"
        )

    def test_timer_pending_decreases_after_fire(self):
        timer = TimerThread()
        timer.start()
        try:
            timer.schedule(0.01, lambda: 1)
            time.sleep(0.05)
            self.assertEqual(
                timer.pending(),
                0,
                "TimerThread.pending should decrease after fire"
            )
        finally:
            timer.stop()

    def test_timer_handles_immediate_fire(self):
        timer = TimerThread()
        timer.start()
        fired = []
        try:
            timer.schedule(0.0, lambda: fired.append(1))
            time.sleep(0.02)
            self.assertEqual(
                len(fired),
                1,
                "TimerThread should handle immediate fire"
            )
        finally:
            timer.stop()

    def test_timer_repr_shows_pending(self):
        timer = TimerThread()
        timer.start()
        try:
            timer.schedule(10.0, lambda: 1)
            self.assertIn(
                "1",
                repr(timer),
                "TimerThread repr should show pending"
            )
        finally:
            timer.stop()

    def test_timer_is_thread_safe(self):
        timer = TimerThread()
        timer.start()
        fired = []
        lock = threading.Lock()
        def append():
            with lock:
                fired.append(1)
        try:
            threads = []
            for _ in range(10):
                t = threading.Thread(
                    target=lambda: timer.schedule(0.01, append)
                )
                threads.append(t)
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            time.sleep(0.1)
            self.assertEqual(
                len(fired),
                10,
                "TimerThread should be thread-safe"
            )
        finally:
            timer.stop()


if __name__ == "__main__":
    unittest.main()
