# -*- coding: utf-8 -*-
"""
Optional monad for null-free optional values.

Optional represents a value that may or may not be present.
This eliminates null references by forcing explicit handling of absence.

Example usage:
    def find_user(user_id):
        if user_id in database:
            return Some(database[user_id])
        return Empty()

    result = find_user(123)
    if result.present():
        user = result.content()
    else:
        user = result.otherwise(default_user)
"""
from abc import ABC, abstractmethod


class Optional(ABC):
    """
    Abstract base for Optional monad representing presence or absence.

    Optional forces explicit handling of both present and absent cases,
    eliminating null references from optional value handling.

    Example usage:
        result = find_something()
        if result.present():
            data = result.content()
        else:
            data = result.otherwise(default)
    """

    @abstractmethod
    def present(self):
        """
        Query whether value is present.

        Returns:
            bool: True if Some (present), False if Empty (absent)
        """
        pass

    @abstractmethod
    def content(self):
        """
        Extract the present value.

        Returns:
            object: The wrapped value

        Raises:
            RuntimeError: If called on Empty (absent)
        """
        pass

    @abstractmethod
    def otherwise(self, default):
        """
        Extract value or return default if absent.

        Args:
            default: Value to return if absent

        Returns:
            object: Present value or default
        """
        pass

    @abstractmethod
    def map(self, func):
        """
        Transform the value if present.

        Args:
            func: Function to apply to present value

        Returns:
            Optional: Some with transformed value, or unchanged Empty
        """
        pass

    @abstractmethod
    def flatmap(self, func):
        """
        Chain with another Optional-returning function.

        Args:
            func: Function returning Optional to chain

        Returns:
            Optional: Result of chained function, or unchanged Empty
        """
        pass


class Some(Optional):
    """
    Present value in an Optional monad.

    Some wraps a value that is definitely present and provides
    transformation operations that preserve the present state.

    Example usage:
        value = Some(42)
        doubled = value.map(lambda x: x * 2)
        print(doubled.content())  # 84
    """

    def __init__(self, item):
        """
        Create a Some with the present value.

        Args:
            item: The value to wrap
        """
        self._item = item

    def present(self):
        """
        Returns True for Some instances.

        Returns:
            bool: Always True
        """
        return True

    def content(self):
        """
        Extract the present value.

        Returns:
            object: The wrapped value
        """
        return self._item

    def otherwise(self, default):
        """
        Returns the present value, ignoring default.

        Args:
            default: Ignored

        Returns:
            object: The wrapped value
        """
        return self._item

    def map(self, func):
        """
        Apply func to content and wrap in new Some.

        Args:
            func: Function to apply to present value

        Returns:
            Some: New Some with transformed value
        """
        return Some(func(self._item))

    def flatmap(self, func):
        """
        Apply func which returns Optional.

        Args:
            func: Function returning Optional

        Returns:
            Optional: Result of applying func to content
        """
        return func(self._item)


class Empty(Optional):
    """
    Absent value in an Optional monad.

    Empty represents the absence of a value and short-circuits all
    transformation operations, preserving the absent state.

    Example usage:
        absent = Empty()
        mapped = absent.map(lambda x: x * 2)  # Still Empty
        value = absent.otherwise(0)  # Returns 0
    """

    def __init__(self):
        """Create an Empty instance representing absence."""
        self._marker = True  # EO: at least one attribute

    def present(self):
        """
        Returns False for Empty instances.

        Returns:
            bool: Always False
        """
        return False

    def content(self):
        """
        Raises RuntimeError since Empty has no content.

        Raises:
            RuntimeError: Always, as Empty represents absence
        """
        raise RuntimeError("Cannot extract content from Empty")

    def otherwise(self, default):
        """
        Returns the default value.

        Args:
            default: Value to return

        Returns:
            object: The default value
        """
        return default

    def map(self, func):
        """
        Returns self since Empty cannot be mapped.

        Args:
            func: Ignored

        Returns:
            Empty: Self unchanged
        """
        return self

    def flatmap(self, func):
        """
        Returns self since Empty cannot be flatmapped.

        Args:
            func: Ignored

        Returns:
            Empty: Self unchanged
        """
        return self
