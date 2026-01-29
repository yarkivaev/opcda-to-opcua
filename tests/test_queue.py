# -*- coding: utf-8 -*-
"""
Tests for TaskQueue.
"""
from __future__ import print_function

import logging
import random
import threading
import time
import unittest

from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.task import ReadTask
from opcda_to_mqtt.domain.path import TagPath

logging.disable(logging.CRITICAL)


class TestTaskQueue(unittest.TestCase):
    """Tests for TaskQueue."""

    def test_queue_starts_empty(self):
        queue = TaskQueue()
        self.assertEqual(
            queue.size(),
            0,
            "TaskQueue should start empty"
        )

    def test_queue_put_increases_size(self):
        queue = TaskQueue()
        task = ReadTask(TagPath("Tag"), lambda r: r)
        queue.put(task)
        self.assertEqual(
            queue.size(),
            1,
            "TaskQueue.put should increase size"
        )

    def test_queue_get_returns_put_item(self):
        queue = TaskQueue()
        task = ReadTask(TagPath("Tag"), lambda r: r)
        queue.put(task)
        result = queue.get()
        self.assertIs(
            result,
            task,
            "TaskQueue.get should return put item"
        )

    def test_queue_get_decreases_size(self):
        queue = TaskQueue()
        queue.put(ReadTask(TagPath("Tag"), lambda r: r))
        queue.get()
        self.assertEqual(
            queue.size(),
            0,
            "TaskQueue.get should decrease size"
        )

    def test_queue_is_fifo(self):
        queue = TaskQueue()
        task1 = ReadTask(TagPath("Tag1"), lambda r: r)
        task2 = ReadTask(TagPath("Tag2"), lambda r: r)
        queue.put(task1)
        queue.put(task2)
        first = queue.get()
        self.assertIs(
            first,
            task1,
            "TaskQueue should be FIFO"
        )

    def test_queue_accepts_none_sentinel(self):
        queue = TaskQueue()
        queue.put(None)
        result = queue.get()
        self.assertIsNone(
            result,
            "TaskQueue should accept None sentinel"
        )

    def test_queue_get_blocks_until_item_available(self):
        queue = TaskQueue()
        result = []
        def producer():
            time.sleep(0.01)
            queue.put("item")
        def consumer():
            result.append(queue.get())
        t1 = threading.Thread(target=producer)
        t2 = threading.Thread(target=consumer)
        t2.start()
        t1.start()
        t1.join()
        t2.join()
        self.assertEqual(
            result[0],
            "item",
            "TaskQueue.get should block until item available"
        )

    def test_queue_handles_multiple_producers(self):
        queue = TaskQueue()
        count = random.randint(5, 15)
        threads = []
        for i in range(count):
            t = threading.Thread(target=lambda n=i: queue.put(n))
            threads.append(t)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(
            queue.size(),
            count,
            "TaskQueue should handle multiple producers"
        )

    def test_queue_repr_shows_size(self):
        queue = TaskQueue()
        queue.put(ReadTask(TagPath("Tag"), lambda r: r))
        self.assertIn(
            "1",
            repr(queue),
            "TaskQueue repr should show size"
        )


if __name__ == "__main__":
    unittest.main()
