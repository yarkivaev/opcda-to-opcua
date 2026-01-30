# -*- coding: utf-8 -*-
"""
Tests for TagRead.
"""
from __future__ import print_function

import json
import logging
import random
import string
import unittest

from opcda_to_mqtt.sync.reading import TagRead
from opcda_to_mqtt.domain.path import TagPath
from opcda_to_mqtt.sync.worker import FakeOpcClient

logging.disable(logging.CRITICAL)


class TestTagRead(unittest.TestCase):
    """Tests for TagRead."""

    def test_tag_read_calls_output_with_message(self):
        name = "".join(random.choice(string.ascii_letters) for _ in range(8))
        path = TagPath(name)
        value = random.randint(1, 100)
        source = FakeOpcClient({name: value})
        messages = []
        reading = TagRead(path, source, messages.append, lambda: None)
        reading.publish()
        self.assertEqual(
            len(messages),
            1,
            "TagRead should call output with message"
        )

    def test_tag_read_message_contains_value(self):
        name = "".join(random.choice(string.ascii_letters) for _ in range(6))
        path = TagPath(name)
        value = random.randint(1, 100)
        source = FakeOpcClient({name: value})
        messages = []
        reading = TagRead(path, source, messages.append, lambda: None)
        reading.publish()
        data = json.loads(messages[0])
        self.assertEqual(
            data["value"],
            value,
            "TagRead message should contain value"
        )

    def test_tag_read_message_contains_quality(self):
        name = "".join(random.choice(string.ascii_letters) for _ in range(6))
        path = TagPath(name)
        source = FakeOpcClient({name: random.randint(1, 100)})
        messages = []
        reading = TagRead(path, source, messages.append, lambda: None)
        reading.publish()
        data = json.loads(messages[0])
        self.assertEqual(
            data["quality"],
            "good",
            "TagRead message should contain quality"
        )

    def test_tag_read_calls_reschedule(self):
        name = "".join(random.choice(string.ascii_letters) for _ in range(6))
        path = TagPath(name)
        source = FakeOpcClient({name: random.randint(1, 100)})
        called = []
        reading = TagRead(path, source, lambda m: None, lambda: called.append(1))
        reading.publish()
        self.assertEqual(
            len(called),
            1,
            "TagRead should call reschedule"
        )

    def test_tag_read_repr_shows_path(self):
        name = "".join(random.choice(string.ascii_letters) for _ in range(8))
        path = TagPath(name)
        source = FakeOpcClient({})
        reading = TagRead(path, source, lambda m: None, lambda: None)
        self.assertIn(
            name,
            repr(reading),
            "TagRead repr should show path"
        )

    def test_tag_read_reads_from_source(self):
        name = "".join(random.choice(string.ascii_letters) for _ in range(6))
        path = TagPath(name)
        value = random.randint(100, 200)
        source = FakeOpcClient({name: value})
        messages = []
        reading = TagRead(path, source, messages.append, lambda: None)
        reading.publish()
        data = json.loads(messages[0])
        self.assertEqual(
            data["value"],
            value,
            "TagRead should read value from source"
        )

    def test_tag_read_handles_cyrillic_path(self):
        name = u"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430"
        path = TagPath(name)
        source = FakeOpcClient({name: random.randint(1, 100)})
        messages = []
        reading = TagRead(path, source, messages.append, lambda: None)
        reading.publish()
        self.assertEqual(
            len(messages),
            1,
            "TagRead should handle Cyrillic path"
        )


if __name__ == "__main__":
    unittest.main()
