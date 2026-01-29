# -*- coding: utf-8 -*-
"""
Tests for Worker and FakeWorker.
"""
from __future__ import print_function

import logging
import random
import string
import time
import unittest

from opcda_to_mqtt.sync.worker import FakeWorker
from opcda_to_mqtt.sync.queue import TaskQueue
from opcda_to_mqtt.sync.task import ReadTask
from opcda_to_mqtt.domain.path import TagPath

logging.disable(logging.CRITICAL)


class TestFakeWorker(unittest.TestCase):
    """Tests for FakeWorker."""

    def test_worker_starts_with_no_executed(self):
        queue = TaskQueue()
        worker = FakeWorker(queue, {})
        self.assertEqual(
            len(worker.executed()),
            0,
            "FakeWorker should start with no executed"
        )

    def test_worker_executes_task_from_queue(self):
        queue = TaskQueue()
        results = []
        path = "".join(random.choice(string.ascii_letters) for _ in range(8))
        value = random.randint(1, 100)
        worker = FakeWorker(queue, {path: value})
        worker.start()
        task = ReadTask(TagPath(path), lambda r: results.append(r))
        queue.put(task)
        queue.put(None)
        worker.join()
        self.assertEqual(
            len(results),
            1,
            "FakeWorker should execute task from queue"
        )

    def test_worker_records_executed_tasks(self):
        queue = TaskQueue()
        worker = FakeWorker(queue, {})
        worker.start()
        task = ReadTask(TagPath("Tag"), lambda r: r)
        queue.put(task)
        queue.put(None)
        worker.join()
        self.assertEqual(
            len(worker.executed()),
            1,
            "FakeWorker should record executed tasks"
        )

    def test_worker_stops_on_sentinel(self):
        queue = TaskQueue()
        worker = FakeWorker(queue, {})
        worker.start()
        queue.put(None)
        worker.join()

    def test_worker_executes_multiple_tasks(self):
        queue = TaskQueue()
        count = random.randint(3, 10)
        worker = FakeWorker(queue, {})
        worker.start()
        for i in range(count):
            task = ReadTask(TagPath("Tag%d" % i), lambda r: r)
            queue.put(task)
        queue.put(None)
        worker.join()
        self.assertEqual(
            len(worker.executed()),
            count,
            "FakeWorker should execute multiple tasks"
        )

    def test_worker_uses_configured_readings(self):
        queue = TaskQueue()
        path = "Device.Sensor"
        value = random.randint(1, 1000)
        results = []
        worker = FakeWorker(queue, {path: value})
        worker.start()
        task = ReadTask(TagPath(path), lambda r: results.append(r[0]))
        queue.put(task)
        queue.put(None)
        worker.join()
        self.assertEqual(
            results[0],
            value,
            "FakeWorker should use configured readings"
        )

    def test_worker_handles_cyrillic_path(self):
        queue = TaskQueue()
        path = u"COM1.\u0422\u041c_5104"
        value = random.randint(1, 100)
        results = []
        worker = FakeWorker(queue, {path: value})
        worker.start()
        task = ReadTask(TagPath(path), lambda r: results.append(r))
        queue.put(task)
        queue.put(None)
        worker.join()
        self.assertEqual(
            len(results),
            1,
            "FakeWorker should handle Cyrillic path"
        )

    def test_worker_executed_returns_copy(self):
        queue = TaskQueue()
        worker = FakeWorker(queue, {})
        worker.start()
        queue.put(ReadTask(TagPath("Tag"), lambda r: r))
        queue.put(None)
        worker.join()
        executed = worker.executed()
        executed.append("extra")
        self.assertEqual(
            len(worker.executed()),
            1,
            "FakeWorker.executed should return a copy"
        )


if __name__ == "__main__":
    unittest.main()
