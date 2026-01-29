# -*- coding: utf-8 -*-
"""
Either ADT for representing success or failure.

Example:
    >>> result = Right("success")
    >>> result.fold(lambda e: "error", lambda v: "got: " + v)
    'got: success'

    >>> error = Left(Problem("failed", {"key": "value"}))
    >>> error.fold(lambda e: e.text(), lambda v: "ok")
    'failed (key=value)'
"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod


class Either:
    """
    Abstract base class for Either ADT.

    Either represents a value that can be one of two types:
    Right for success, Left for failure.

    Example:
        >>> def parse(s):
        ...     if s.isdigit():
        ...         return Right(int(s))
        ...     return Left(Problem("not a number", {"input": s}))
        >>> parse("42").fold(lambda e: -1, lambda v: v)
        42
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def fold(self, left, right):
        """
        Apply left function if Left, right function if Right.

        Args:
            left: Function to apply if Left
            right: Function to apply if Right

        Returns:
            Result of applying the appropriate function
        """
        raise NotImplementedError()

    @abstractmethod
    def is_right(self):
        """
        Check if this is a Right value.

        Returns:
            True if Right, False if Left
        """
        raise NotImplementedError()

    @abstractmethod
    def map(self, func):
        """
        Apply function to Right value, pass through Left.

        Args:
            func: Function to apply to Right value

        Returns:
            New Either with transformed Right or original Left
        """
        raise NotImplementedError()

    @abstractmethod
    def flatmap(self, func):
        """
        Apply function returning Either to Right value.

        Args:
            func: Function returning Either to apply to Right value

        Returns:
            Result of function if Right, original Left otherwise
        """
        raise NotImplementedError()


class Right(Either):
    """
    Success case of Either ADT.

    Contains a successful value that can be transformed.

    Example:
        >>> Right(42).map(lambda x: x * 2).fold(lambda e: 0, lambda v: v)
        84
    """

    def __init__(self, content):
        """
        Create a Right with the given content.

        Args:
            content: The successful value to wrap
        """
        self._content = content

    def fold(self, left, right):
        """
        Apply right function to the content.

        Args:
            left: Function to apply if Left (unused)
            right: Function to apply to content

        Returns:
            Result of applying right function to content
        """
        return right(self._content)

    def is_right(self):
        """
        Check if this is a Right value.

        Returns:
            Always True for Right
        """
        return True

    def map(self, func):
        """
        Apply function to the content.

        Args:
            func: Function to apply to content

        Returns:
            New Right with transformed content
        """
        return Right(func(self._content))

    def flatmap(self, func):
        """
        Apply function returning Either to content.

        Args:
            func: Function returning Either

        Returns:
            Result of applying function to content
        """
        return func(self._content)

    def content(self):
        """
        Get the wrapped content.

        Returns:
            The successful value
        """
        return self._content

    def __eq__(self, other):
        """
        Check equality with another Right.

        Args:
            other: Object to compare

        Returns:
            True if other is Right with same content
        """
        if not isinstance(other, Right):
            return False
        return self._content == other._content

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Right and its content
        """
        return "Right(%r)" % self._content


class Left(Either):
    """
    Failure case of Either ADT.

    Contains an error that is passed through transformations.

    Example:
        >>> Left(Problem("oops", {})).map(lambda x: x * 2).is_right()
        False
    """

    def __init__(self, error):
        """
        Create a Left with the given error.

        Args:
            error: The Problem describing the failure
        """
        self._error = error

    def fold(self, left, right):
        """
        Apply left function to the error.

        Args:
            left: Function to apply to error
            right: Function to apply if Right (unused)

        Returns:
            Result of applying left function to error
        """
        return left(self._error)

    def is_right(self):
        """
        Check if this is a Right value.

        Returns:
            Always False for Left
        """
        return False

    def map(self, func):
        """
        Pass through the Left unchanged.

        Args:
            func: Function to apply (unused)

        Returns:
            This Left unchanged
        """
        return self

    def flatmap(self, func):
        """
        Pass through the Left unchanged.

        Args:
            func: Function to apply (unused)

        Returns:
            This Left unchanged
        """
        return self

    def error(self):
        """
        Get the wrapped error.

        Returns:
            The Problem describing the failure
        """
        return self._error

    def __eq__(self, other):
        """
        Check equality with another Left.

        Args:
            other: Object to compare

        Returns:
            True if other is Left with same error
        """
        if not isinstance(other, Left):
            return False
        return self._error == other._error

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Left and its error
        """
        return "Left(%r)" % self._error


class Problem:
    """
    Error description with context information.

    Contains a message and a dictionary of context key-value pairs.

    Example:
        >>> p = Problem("connection failed", {"host": "localhost", "port": 1883})
        >>> p.text()
        'connection failed (host=localhost, port=1883)'
    """

    def __init__(self, message, context):
        """
        Create a Problem with message and context.

        Args:
            message: Error message string
            context: Dictionary of context key-value pairs
        """
        self._message = message
        self._context = context

    def text(self):
        """
        Format the problem as a string.

        Returns:
            Message with context in parentheses
        """
        if not self._context:
            return self._message
        pairs = ", ".join(
            "%s=%s" % (k, v) for k, v in sorted(self._context.items())
        )
        return "%s (%s)" % (self._message, pairs)

    def message(self):
        """
        Get the error message.

        Returns:
            The error message string
        """
        return self._message

    def context(self):
        """
        Get the context dictionary.

        Returns:
            Dictionary of context key-value pairs
        """
        return dict(self._context)

    def __eq__(self, other):
        """
        Check equality with another Problem.

        Args:
            other: Object to compare

        Returns:
            True if other is Problem with same message and context
        """
        if not isinstance(other, Problem):
            return False
        return (
            self._message == other._message and
            self._context == other._context
        )

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Problem message and context
        """
        return "Problem(%r, %r)" % (self._message, self._context)
