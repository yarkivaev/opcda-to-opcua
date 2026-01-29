# -*- coding: utf-8 -*-
"""
Optional ADT for representing presence or absence of a value.

Example:
    >>> some = Some("hello")
    >>> some.fold(lambda: "empty", lambda v: "got: " + v)
    'got: hello'

    >>> empty = Empty()
    >>> empty.fold(lambda: "empty", lambda v: "got: " + v)
    'empty'
"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod


class Optional:
    """
    Abstract base class for Optional ADT.

    Optional represents a value that may or may not be present:
    Some for present, Empty for absent.

    Example:
        >>> def find(items, key):
        ...     if key in items:
        ...         return Some(items[key])
        ...     return Empty()
        >>> find({"a": 1}, "a").fold(lambda: 0, lambda v: v)
        1
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def fold(self, empty, some):
        """
        Apply empty function if Empty, some function if Some.

        Args:
            empty: Function to call if Empty (no arguments)
            some: Function to apply if Some (receives value)

        Returns:
            Result of applying the appropriate function
        """
        raise NotImplementedError()

    @abstractmethod
    def is_present(self):
        """
        Check if this is a Some value.

        Returns:
            True if Some, False if Empty
        """
        raise NotImplementedError()

    @abstractmethod
    def map(self, func):
        """
        Apply function to Some value, pass through Empty.

        Args:
            func: Function to apply to Some value

        Returns:
            New Optional with transformed Some or Empty
        """
        raise NotImplementedError()

    @abstractmethod
    def flatmap(self, func):
        """
        Apply function returning Optional to Some value.

        Args:
            func: Function returning Optional to apply to Some value

        Returns:
            Result of function if Some, Empty otherwise
        """
        raise NotImplementedError()

    @abstractmethod
    def otherwise(self, default):
        """
        Get value or default if Empty.

        Args:
            default: Value to return if Empty

        Returns:
            Contained value if Some, default if Empty
        """
        raise NotImplementedError()


class Some(Optional):
    """
    Present case of Optional ADT.

    Contains a value that can be transformed.

    Example:
        >>> Some(42).map(lambda x: x * 2).fold(lambda: 0, lambda v: v)
        84
    """

    def __init__(self, content):
        """
        Create a Some with the given content.

        Args:
            content: The value to wrap
        """
        self._content = content

    def fold(self, empty, some):
        """
        Apply some function to the content.

        Args:
            empty: Function to call if Empty (unused)
            some: Function to apply to content

        Returns:
            Result of applying some function to content
        """
        return some(self._content)

    def is_present(self):
        """
        Check if this is a Some value.

        Returns:
            Always True for Some
        """
        return True

    def map(self, func):
        """
        Apply function to the content.

        Args:
            func: Function to apply to content

        Returns:
            New Some with transformed content
        """
        return Some(func(self._content))

    def flatmap(self, func):
        """
        Apply function returning Optional to content.

        Args:
            func: Function returning Optional

        Returns:
            Result of applying function to content
        """
        return func(self._content)

    def otherwise(self, default):
        """
        Get the contained value.

        Args:
            default: Default value (unused)

        Returns:
            The contained value
        """
        return self._content

    def content(self):
        """
        Get the wrapped content.

        Returns:
            The contained value
        """
        return self._content

    def __eq__(self, other):
        """
        Check equality with another Some.

        Args:
            other: Object to compare

        Returns:
            True if other is Some with same content
        """
        if not isinstance(other, Some):
            return False
        return self._content == other._content

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Some and its content
        """
        return "Some(%r)" % self._content


class Empty(Optional):
    """
    Absent case of Optional ADT.

    Represents the absence of a value.

    Example:
        >>> Empty().map(lambda x: x * 2).is_present()
        False
    """

    def fold(self, empty, some):
        """
        Call the empty function.

        Args:
            empty: Function to call
            some: Function to apply if Some (unused)

        Returns:
            Result of calling empty function
        """
        return empty()

    def is_present(self):
        """
        Check if this is a Some value.

        Returns:
            Always False for Empty
        """
        return False

    def map(self, func):
        """
        Pass through Empty unchanged.

        Args:
            func: Function to apply (unused)

        Returns:
            Empty
        """
        return Empty()

    def flatmap(self, func):
        """
        Pass through Empty unchanged.

        Args:
            func: Function to apply (unused)

        Returns:
            Empty
        """
        return Empty()

    def otherwise(self, default):
        """
        Get the default value.

        Args:
            default: Value to return

        Returns:
            The default value
        """
        return default

    def __eq__(self, other):
        """
        Check equality with another Empty.

        Args:
            other: Object to compare

        Returns:
            True if other is Empty
        """
        return isinstance(other, Empty)

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing Empty
        """
        return "Empty()"
