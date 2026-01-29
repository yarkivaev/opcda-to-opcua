# -*- coding: utf-8 -*-
"""
Tests for Milliseconds domain object.
"""
from __future__ import print_function

import logging
import random
import unittest

from opcda_to_mqtt.domain.interval import Milliseconds

logging.disable(logging.CRITICAL)


class TestMilliseconds(unittest.TestCase):
    """Tests for Milliseconds."""

    def test_milliseconds_amount_returns_value(self):
        amount = random.randint(1, 10000)
        self.assertEqual(
            Milliseconds(amount).amount(),
            amount,
            "Milliseconds.amount should return value"
        )

    def test_milliseconds_seconds_converts_correctly(self):
        amount = random.randint(100, 5000)
        self.assertEqual(
            Milliseconds(amount).seconds(),
            amount / 1000.0,
            "Milliseconds.seconds should convert to seconds"
        )

    def test_milliseconds_seconds_for_1000_equals_1(self):
        self.assertEqual(
            Milliseconds(1000).seconds(),
            1.0,
            "1000 milliseconds should equal 1 second"
        )

    def test_milliseconds_seconds_for_500_equals_half(self):
        self.assertEqual(
            Milliseconds(500).seconds(),
            0.5,
            "500 milliseconds should equal 0.5 seconds"
        )

    def test_milliseconds_raises_on_zero(self):
        with self.assertRaises(ValueError):
            Milliseconds(0)

    def test_milliseconds_raises_on_negative(self):
        with self.assertRaises(ValueError):
            Milliseconds(-1)

    def test_milliseconds_raises_on_large_negative(self):
        with self.assertRaises(ValueError):
            Milliseconds(random.randint(-10000, -1))

    def test_milliseconds_equals_another_with_same_amount(self):
        amount = random.randint(1, 10000)
        self.assertEqual(
            Milliseconds(amount),
            Milliseconds(amount),
            "Milliseconds with same amount should be equal"
        )

    def test_milliseconds_not_equals_different_amount(self):
        self.assertNotEqual(
            Milliseconds(random.randint(1, 100)),
            Milliseconds(random.randint(200, 300)),
            "Milliseconds with different amounts should not be equal"
        )

    def test_milliseconds_repr_shows_amount(self):
        amount = random.randint(1, 1000)
        self.assertIn(
            str(amount),
            repr(Milliseconds(amount)),
            "Milliseconds repr should show amount"
        )


if __name__ == "__main__":
    unittest.main()
