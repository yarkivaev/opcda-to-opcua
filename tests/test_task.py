# -*- coding: utf-8 -*-
"""
Tests for Task and ReadTask.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.sync.task import ReadTask
from opcda_to_mqtt.sync.worker import FakeOpcClient
from opcda_to_mqtt.domain.path import TagPath

logging.disable(logging.CRITICAL)


class TestReadTask(unittest.TestCase):
    """Tests for ReadTask."""

    def test_read_task_execute_calls_client_read(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(10))
        tag = TagPath(path)
        value = random.randint(1, 1000)
        client = FakeOpcClient({path: value})
        results = []
        callback = lambda r: results.append(r)
        task = ReadTask(tag, callback)
        task.execute(client)
        self.assertEqual(
            len(results),
            1,
            "ReadTask.execute should call client and callback"
        )

    def test_read_task_execute_passes_result_to_callback(self):
        path = "Tag.Path"
        value = random.randint(1, 100)
        client = FakeOpcClient({path: value})
        results = []
        task = ReadTask(TagPath(path), lambda r: results.append(r))
        task.execute(client)
        self.assertEqual(
            results[0][0],
            value,
            "ReadTask should pass read result to callback"
        )

    def test_read_task_tag_returns_tagpath(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(8))
        tag = TagPath(path)
        task = ReadTask(tag, lambda r: r)
        self.assertEqual(
            task.tag(),
            tag,
            "ReadTask.tag should return TagPath"
        )

    def test_read_task_handles_cyrillic_path(self):
        path = u"COM1.\u0422\u041c_5104"
        client = FakeOpcClient({path: 42})
        results = []
        task = ReadTask(TagPath(path), lambda r: results.append(r))
        task.execute(client)
        self.assertEqual(
            len(results),
            1,
            "ReadTask should handle Cyrillic path"
        )

    def test_read_task_repr_shows_tag(self):
        path = "Device.Sensor"
        task = ReadTask(TagPath(path), lambda r: r)
        self.assertIn(
            path,
            repr(task),
            "ReadTask repr should show tag"
        )


class TestFakeOpcClient(unittest.TestCase):
    """Tests for FakeOpcClient."""

    def test_fake_client_read_returns_configured_value(self):
        path = "".join(random.choice(string.ascii_letters) for _ in range(8))
        value = random.randint(1, 1000)
        client = FakeOpcClient({path: value})
        result = client.read(path, sync=True)
        self.assertEqual(
            result[0],
            value,
            "FakeOpcClient.read should return configured value"
        )

    def test_fake_client_read_returns_good_quality(self):
        client = FakeOpcClient({"tag": 1})
        result = client.read("tag", sync=True)
        self.assertEqual(
            result[1],
            "Good",
            "FakeOpcClient.read should return Good quality"
        )

    def test_fake_client_read_returns_default_for_unknown(self):
        client = FakeOpcClient({})
        path = "".join(random.choice(string.ascii_letters) for _ in range(10))
        result = client.read(path, sync=True)
        self.assertEqual(
            result[0],
            0,
            "FakeOpcClient.read should return 0 for unknown tag"
        )

    def test_fake_client_connect_does_not_raise(self):
        client = FakeOpcClient({})
        client.connect("ProgID")

    def test_fake_client_close_does_not_raise(self):
        client = FakeOpcClient({})
        client.close()


if __name__ == "__main__":
    unittest.main()
