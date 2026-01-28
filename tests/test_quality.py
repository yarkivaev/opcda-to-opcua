# -*- coding: utf-8 -*-
"""
Unit tests for Quality domain object.
"""
import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.domain.quality import OpcQuality


class OpcQualityReturnsCodeTest(unittest.TestCase):
    """OpcQuality returns code."""

    def test(self):
        code = random.randint(0, 255)
        quality = OpcQuality(code)
        self.assertEqual(
            quality.code(),
            code,
            "OpcQuality must return code"
        )


class OpcQualityGoodForHighCodeTest(unittest.TestCase):
    """OpcQuality reports good for high code."""

    def test(self):
        code = random.randint(192, 255)
        quality = OpcQuality(code)
        self.assertTrue(
            quality.good(),
            "OpcQuality must report good for code >= 192"
        )


class OpcQualityNotGoodForLowCodeTest(unittest.TestCase):
    """OpcQuality reports not good for low code."""

    def test(self):
        code = random.randint(0, 191)
        quality = OpcQuality(code)
        self.assertFalse(
            quality.good(),
            "OpcQuality must report not good for code < 192"
        )


class OpcQualityBadForVeryLowCodeTest(unittest.TestCase):
    """OpcQuality reports bad for very low code."""

    def test(self):
        code = random.randint(0, 63)
        quality = OpcQuality(code)
        self.assertTrue(
            quality.bad(),
            "OpcQuality must report bad for code < 64"
        )


class OpcQualityNotBadForHighCodeTest(unittest.TestCase):
    """OpcQuality reports not bad for high code."""

    def test(self):
        code = random.randint(64, 255)
        quality = OpcQuality(code)
        self.assertFalse(
            quality.bad(),
            "OpcQuality must report not bad for code >= 64"
        )


class OpcQualityUncertainForMiddleCodeTest(unittest.TestCase):
    """OpcQuality reports uncertain for middle code."""

    def test(self):
        code = random.randint(64, 191)
        quality = OpcQuality(code)
        self.assertTrue(
            quality.uncertain(),
            "OpcQuality must report uncertain for 64 <= code < 192"
        )


class OpcQualityNotUncertainForGoodCodeTest(unittest.TestCase):
    """OpcQuality reports not uncertain for good code."""

    def test(self):
        code = random.randint(192, 255)
        quality = OpcQuality(code)
        self.assertFalse(
            quality.uncertain(),
            "OpcQuality must report not uncertain for code >= 192"
        )


class OpcQualityNotUncertainForBadCodeTest(unittest.TestCase):
    """OpcQuality reports not uncertain for bad code."""

    def test(self):
        code = random.randint(0, 63)
        quality = OpcQuality(code)
        self.assertFalse(
            quality.uncertain(),
            "OpcQuality must report not uncertain for code < 64"
        )


class OpcQualityBoundaryGoodAt192Test(unittest.TestCase):
    """OpcQuality boundary: 192 is good."""

    def test(self):
        quality = OpcQuality(192)
        self.assertTrue(
            quality.good(),
            "OpcQuality 192 must be good"
        )


class OpcQualityBoundaryNotGoodAt191Test(unittest.TestCase):
    """OpcQuality boundary: 191 is not good."""

    def test(self):
        quality = OpcQuality(191)
        self.assertFalse(
            quality.good(),
            "OpcQuality 191 must not be good"
        )


class OpcQualityBoundaryBadAt63Test(unittest.TestCase):
    """OpcQuality boundary: 63 is bad."""

    def test(self):
        quality = OpcQuality(63)
        self.assertTrue(
            quality.bad(),
            "OpcQuality 63 must be bad"
        )


class OpcQualityBoundaryNotBadAt64Test(unittest.TestCase):
    """OpcQuality boundary: 64 is not bad."""

    def test(self):
        quality = OpcQuality(64)
        self.assertFalse(
            quality.bad(),
            "OpcQuality 64 must not be bad"
        )


class OpcQualityEqualityTest(unittest.TestCase):
    """OpcQuality equality compares codes."""

    def test(self):
        code = random.randint(0, 255)
        q1 = OpcQuality(code)
        q2 = OpcQuality(code)
        self.assertEqual(
            q1,
            q2,
            "OpcQualities with same code must be equal"
        )


class OpcQualityInequalityTest(unittest.TestCase):
    """OpcQuality inequality for different codes."""

    def test(self):
        q1 = OpcQuality(192)
        q2 = OpcQuality(0)
        self.assertNotEqual(
            q1,
            q2,
            "OpcQualities with different codes must not be equal"
        )


class OpcQualityHashConsistencyTest(unittest.TestCase):
    """OpcQuality hash is consistent with equality."""

    def test(self):
        code = random.randint(0, 255)
        q1 = OpcQuality(code)
        q2 = OpcQuality(code)
        self.assertEqual(
            hash(q1),
            hash(q2),
            "Equal OpcQualities must have equal hashes"
        )


if __name__ == "__main__":
    unittest.main()
