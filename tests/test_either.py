# -*- coding: utf-8 -*-
"""
Tests for Either ADT.
"""
from __future__ import print_function

import logging
import random
import string
import unittest

from opcda_to_mqtt.result.either import Either, Right, Left, Problem

logging.disable(logging.CRITICAL)


class TestRight(unittest.TestCase):
    """Tests for Right success case."""

    def test_right_fold_applies_right_function_to_content(self):
        content = random.randint(1, 1000)
        result = Right(content).fold(
            lambda e: "error",
            lambda v: v * 2
        )
        self.assertEqual(
            result,
            content * 2,
            "Right.fold should apply right function"
        )

    def test_right_is_right_returns_true(self):
        content = "".join(random.choice(string.ascii_letters) for _ in range(8))
        self.assertTrue(
            Right(content).is_right(),
            "Right.is_right should return True"
        )

    def test_right_map_transforms_content(self):
        content = random.randint(1, 100)
        result = Right(content).map(lambda x: x + 10)
        self.assertEqual(
            result.fold(lambda e: 0, lambda v: v),
            content + 10,
            "Right.map should transform content"
        )

    def test_right_flatmap_returns_function_result(self):
        content = random.randint(1, 50)
        result = Right(content).flatmap(lambda x: Right(x * 3))
        self.assertEqual(
            result.fold(lambda e: 0, lambda v: v),
            content * 3,
            "Right.flatmap should return function result"
        )

    def test_right_content_returns_wrapped_value(self):
        content = "".join(random.choice(string.ascii_letters) for _ in range(10))
        self.assertEqual(
            Right(content).content(),
            content,
            "Right.content should return wrapped value"
        )

    def test_right_equals_another_right_with_same_content(self):
        content = random.randint(1, 1000)
        self.assertEqual(
            Right(content),
            Right(content),
            "Rights with same content should be equal"
        )

    def test_right_not_equals_right_with_different_content(self):
        self.assertNotEqual(
            Right(random.randint(1, 100)),
            Right(random.randint(200, 300)),
            "Rights with different content should not be equal"
        )

    def test_right_not_equals_left(self):
        content = random.randint(1, 100)
        self.assertNotEqual(
            Right(content),
            Left(Problem("error", {})),
            "Right should not equal Left"
        )

    def test_right_repr_shows_content(self):
        content = random.randint(1, 100)
        self.assertIn(
            str(content),
            repr(Right(content)),
            "Right repr should show content"
        )


class TestLeft(unittest.TestCase):
    """Tests for Left failure case."""

    def test_left_fold_applies_left_function_to_error(self):
        message = "".join(random.choice(string.ascii_letters) for _ in range(8))
        error = Problem(message, {})
        result = Left(error).fold(
            lambda e: e.message(),
            lambda v: "success"
        )
        self.assertEqual(
            result,
            message,
            "Left.fold should apply left function"
        )

    def test_left_is_right_returns_false(self):
        error = Problem("error", {})
        self.assertFalse(
            Left(error).is_right(),
            "Left.is_right should return False"
        )

    def test_left_map_passes_through_unchanged(self):
        error = Problem("error", {"key": "value"})
        left = Left(error)
        result = left.map(lambda x: x * 2)
        self.assertIs(
            result,
            left,
            "Left.map should pass through unchanged"
        )

    def test_left_flatmap_passes_through_unchanged(self):
        error = Problem("error", {})
        left = Left(error)
        result = left.flatmap(lambda x: Right(x * 2))
        self.assertIs(
            result,
            left,
            "Left.flatmap should pass through unchanged"
        )

    def test_left_error_returns_wrapped_problem(self):
        error = Problem("test", {"a": "b"})
        self.assertEqual(
            Left(error).error(),
            error,
            "Left.error should return wrapped Problem"
        )

    def test_left_equals_another_left_with_same_error(self):
        error = Problem("same", {"k": "v"})
        self.assertEqual(
            Left(error),
            Left(error),
            "Lefts with same error should be equal"
        )

    def test_left_not_equals_left_with_different_error(self):
        self.assertNotEqual(
            Left(Problem("one", {})),
            Left(Problem("two", {})),
            "Lefts with different errors should not be equal"
        )

    def test_left_repr_shows_error(self):
        error = Problem("test-message", {})
        self.assertIn(
            "test-message",
            repr(Left(error)),
            "Left repr should show error"
        )


class TestProblem(unittest.TestCase):
    """Tests for Problem error description."""

    def test_problem_text_returns_message_when_no_context(self):
        message = "".join(random.choice(string.ascii_letters) for _ in range(12))
        self.assertEqual(
            Problem(message, {}).text(),
            message,
            "Problem.text should return message alone when no context"
        )

    def test_problem_text_includes_context(self):
        message = "failed"
        context = {"host": "localhost", "port": str(random.randint(1000, 9999))}
        text = Problem(message, context).text()
        self.assertIn(
            "host=localhost",
            text,
            "Problem.text should include context"
        )

    def test_problem_message_returns_original_message(self):
        message = "".join(random.choice(string.ascii_letters) for _ in range(10))
        self.assertEqual(
            Problem(message, {"a": "b"}).message(),
            message,
            "Problem.message should return original message"
        )

    def test_problem_context_returns_copy_of_context(self):
        context = {"key": "value"}
        problem = Problem("msg", context)
        returned = problem.context()
        self.assertEqual(
            returned,
            context,
            "Problem.context should return context"
        )

    def test_problem_context_is_copy_not_original(self):
        context = {"key": "value"}
        problem = Problem("msg", context)
        returned = problem.context()
        returned["new"] = "added"
        self.assertNotIn(
            "new",
            problem.context(),
            "Problem.context should return a copy"
        )

    def test_problem_equals_another_with_same_values(self):
        self.assertEqual(
            Problem("msg", {"a": "b"}),
            Problem("msg", {"a": "b"}),
            "Problems with same values should be equal"
        )

    def test_problem_not_equals_different_message(self):
        self.assertNotEqual(
            Problem("one", {}),
            Problem("two", {}),
            "Problems with different messages should not be equal"
        )

    def test_problem_not_equals_different_context(self):
        self.assertNotEqual(
            Problem("msg", {"a": "1"}),
            Problem("msg", {"a": "2"}),
            "Problems with different contexts should not be equal"
        )

    def test_problem_repr_shows_message_and_context(self):
        rep = repr(Problem("test", {"k": "v"}))
        self.assertIn(
            "test",
            rep,
            "Problem repr should show message"
        )


if __name__ == "__main__":
    unittest.main()
