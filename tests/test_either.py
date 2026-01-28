# -*- coding: utf-8 -*-
"""
Unit tests for Either monad.

Tests follow Elegant Objects testing principles:
- One assertion per test
- Test names are full English sentences
- Random inputs where applicable
- No setUp/tearDown idioms
- No shared constants between tests
"""
import unittest
import random
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from opcda_to_opcua.result.either import Either, Right, Left, Problem


class RightReportsSuccessfulAsTrueTest(unittest.TestCase):
    """Right reports successful as true."""

    def test(self):
        content = random.randint(-1000, 1000)
        result = Right(content)
        self.assertTrue(
            result.successful(),
            "Right must report successful as true"
        )


class RightReturnsWrappedContentTest(unittest.TestCase):
    """Right returns wrapped content."""

    def test(self):
        content = u"\u0422\u0435\u043c\u043f\u0435\u0440\u0430\u0442\u0443\u0440\u0430"
        result = Right(content)
        self.assertEqual(
            result.value(),
            content,
            "Right must return wrapped content"
        )


class RightReturnsIntegerContentTest(unittest.TestCase):
    """Right returns integer content unchanged."""

    def test(self):
        content = random.randint(-999999, 999999)
        result = Right(content)
        self.assertEqual(
            result.value(),
            content,
            "Right must return integer content unchanged"
        )


class RightReturnsFloatContentTest(unittest.TestCase):
    """Right returns float content unchanged."""

    def test(self):
        content = random.uniform(-1000.0, 1000.0)
        result = Right(content)
        self.assertAlmostEqual(
            result.value(),
            content,
            places=10,
            msg="Right must return float content unchanged"
        )


class RightRaisesOnProblemExtractionTest(unittest.TestCase):
    """Right raises RuntimeError on problem extraction."""

    def test(self):
        result = Right(random.randint(0, 100))
        with self.assertRaises(RuntimeError):
            result.problem()


class RightMapsContentWithFunctionTest(unittest.TestCase):
    """Right maps content with function."""

    def test(self):
        content = random.randint(1, 100)
        result = Right(content)
        doubled = result.map(lambda x: x * 2)
        self.assertEqual(
            doubled.value(),
            content * 2,
            "Right must map content with function"
        )


class RightMapsToNewRightInstanceTest(unittest.TestCase):
    """Right map returns new Right instance."""

    def test(self):
        original = Right(random.randint(1, 100))
        mapped = original.map(lambda x: x)
        self.assertIsNot(
            original,
            mapped,
            "Right map must return new instance"
        )


class RightFlatmapsToNewEitherTest(unittest.TestCase):
    """Right flatmaps to new Either."""

    def test(self):
        result = Right(random.randint(10, 100))
        chained = result.flatmap(lambda x: Right(x + 5) if x > 5 else Left(Problem("too small", "")))
        self.assertTrue(
            chained.successful(),
            "Right must flatmap to new Either"
        )


class RightFlatmapsToLeftOnConditionTest(unittest.TestCase):
    """Right flatmaps to Left when condition fails."""

    def test(self):
        result = Right(random.randint(-10, 0))
        chained = result.flatmap(lambda x: Right(x) if x > 50 else Left(Problem("too small", "")))
        self.assertFalse(
            chained.successful(),
            "Right must flatmap to Left when condition fails"
        )


class LeftReportsSuccessfulAsFalseTest(unittest.TestCase):
    """Left reports successful as false."""

    def test(self):
        error = Problem("Connection timeout after %d ms" % random.randint(1000, 5000), "")
        result = Left(error)
        self.assertFalse(
            result.successful(),
            "Left must report successful as false"
        )


class LeftReturnsWrappedErrorTest(unittest.TestCase):
    """Left returns wrapped error."""

    def test(self):
        message = u"\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f"
        error = Problem(message, "")
        result = Left(error)
        self.assertEqual(
            result.problem().message(),
            message,
            "Left must return wrapped error"
        )


class LeftRaisesOnValueExtractionTest(unittest.TestCase):
    """Left raises RuntimeError on value extraction."""

    def test(self):
        result = Left(Problem("error", ""))
        with self.assertRaises(RuntimeError):
            result.value()


class LeftMapReturnsSelfTest(unittest.TestCase):
    """Left map returns self unchanged."""

    def test(self):
        error = Problem("original error", "")
        result = Left(error)
        mapped = result.map(lambda x: x * 2)
        self.assertIs(
            mapped,
            result,
            "Left map must return self unchanged"
        )


class LeftFlatmapReturnsSelfTest(unittest.TestCase):
    """Left flatmap returns self unchanged."""

    def test(self):
        error = Problem("original error", "")
        result = Left(error)
        chained = result.flatmap(lambda x: Right(x * 2))
        self.assertIs(
            chained,
            result,
            "Left flatmap must return self unchanged"
        )


class LeftPreservesErrorThroughMapTest(unittest.TestCase):
    """Left preserves error through map operation."""

    def test(self):
        message = "error_%d" % random.randint(1000, 9999)
        result = Left(Problem(message, ""))
        mapped = result.map(lambda x: x * 2)
        self.assertEqual(
            mapped.problem().message(),
            message,
            "Left must preserve error through map"
        )


class ProblemReturnsMessageTest(unittest.TestCase):
    """Problem returns message."""

    def test(self):
        message = "Connection failed %d" % random.randint(1, 100)
        problem = Problem(message, "")
        self.assertEqual(
            problem.message(),
            message,
            "Problem must return message"
        )


class ProblemReturnsContextTest(unittest.TestCase):
    """Problem returns context."""

    def test(self):
        context = "host=192.168.%d.%d" % (random.randint(0, 255), random.randint(0, 255))
        problem = Problem("error", context)
        self.assertEqual(
            problem.context(),
            context,
            "Problem must return context"
        )


class ProblemFormatsAsStringWithContextTest(unittest.TestCase):
    """Problem formats as string with context."""

    def test(self):
        message = "Failed"
        context = "reason_%d" % random.randint(1, 100)
        problem = Problem(message, context)
        self.assertEqual(
            str(problem),
            "%s: %s" % (message, context),
            "Problem must format as string with context"
        )


class ProblemFormatsAsStringWithoutContextTest(unittest.TestCase):
    """Problem formats as string without context."""

    def test(self):
        message = "Failed_%d" % random.randint(1, 100)
        problem = Problem(message, "")
        self.assertEqual(
            str(problem),
            message,
            "Problem must format as string without context"
        )


class ProblemHandlesUnicodeMessageTest(unittest.TestCase):
    """Problem handles unicode message."""

    def test(self):
        message = u"\u041e\u0448\u0438\u0431\u043a\u0430"
        problem = Problem(message, "")
        self.assertEqual(
            problem.message(),
            message,
            "Problem must handle unicode message"
        )


class ProblemHandlesUnicodeContextTest(unittest.TestCase):
    """Problem handles unicode context."""

    def test(self):
        context = u"\u043a\u043e\u043d\u0442\u0435\u043a\u0441\u0442"
        problem = Problem("error", context)
        self.assertEqual(
            problem.context(),
            context,
            "Problem must handle unicode context"
        )


if __name__ == "__main__":
    unittest.main()
