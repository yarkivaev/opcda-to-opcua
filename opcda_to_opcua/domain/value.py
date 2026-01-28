# -*- coding: utf-8 -*-
"""
Value abstraction for OPC data representation.

Value encapsulates the content and type information of OPC data
without exposing its raw form.

Example usage:
    value = TagValue(42, IntVariant())
    print(value.content())  # 42
    print(value.variant().name())  # Int32
"""
from abc import ABC, abstractmethod


class Value(ABC):
    """
    Interface for OPC value representation.

    Value encapsulates both the data content and its variant type.
    Implementations must be immutable.
    """

    @abstractmethod
    def content(self):
        """
        Extract the raw value content.

        Returns:
            object: The encapsulated value in Python form
        """
        pass

    @abstractmethod
    def variant(self):
        """
        Extract the variant type descriptor.

        Returns:
            Variant: The type information for this value
        """
        pass


class TagValue(Value):
    """
    Immutable OPC value with type information.

    TagValue wraps a Python value together with its OPC variant type,
    enabling type-safe handling of OPC data.

    Example usage:
        value = TagValue(3.14, FloatVariant())
        print(value.content())  # 3.14
        print(value.variant().code())  # 4
    """

    def __init__(self, content, variant):
        """
        Create a TagValue with content and variant type.

        Args:
            content: The Python value to wrap
            variant (Variant): The OPC variant type
        """
        self._content = content
        self._variant = variant

    def content(self):
        """
        Extract the raw value content.

        Returns:
            object: The wrapped Python value
        """
        return self._content

    def variant(self):
        """
        Extract the variant type descriptor.

        Returns:
            Variant: The type information
        """
        return self._variant

    def __eq__(self, other):
        """
        Compare values for equality.

        Args:
            other: Another value to compare

        Returns:
            bool: True if content and variant type match
        """
        if not isinstance(other, TagValue):
            return False
        return (self._content == other._content and
                self._variant.code() == other._variant.code())

    def __hash__(self):
        """
        Compute hash for use in collections.

        Returns:
            int: Hash based on content and variant code
        """
        return hash((self._content, self._variant.code()))
