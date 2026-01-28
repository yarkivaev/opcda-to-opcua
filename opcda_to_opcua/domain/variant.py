# -*- coding: utf-8 -*-
"""
Variant type abstraction for OPC data type representation.

Variant represents the data type of an OPC value, providing
type code and conversion capabilities.

Example usage:
    variant = IntVariant()
    print(variant.code())  # 3 (VT_I4)
    print(variant.name())  # "Int32"
"""
from abc import ABC, abstractmethod


class Variant(ABC):
    """
    Interface for OPC variant type representation.

    Variant encapsulates the type information for OPC values,
    providing type codes compatible with OPC specifications.
    """

    @abstractmethod
    def code(self):
        """
        Extract the OPC variant type code.

        Returns:
            int: OPC variant type code (VT_* constants)
        """
        pass

    @abstractmethod
    def name(self):
        """
        Extract the human-readable type name.

        Returns:
            str: Type name for display
        """
        pass


class IntVariant(Variant):
    """
    32-bit signed integer variant type.

    Example usage:
        variant = IntVariant()
        print(variant.code())  # 3
    """

    def __init__(self):
        """Create an IntVariant instance."""
        self._code = 3  # VT_I4

    def code(self):
        """
        Returns VT_I4 (3) for 32-bit integer.

        Returns:
            int: 3
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "Int32"
        """
        return "Int32"


class UintVariant(Variant):
    """
    32-bit unsigned integer variant type.

    Example usage:
        variant = UintVariant()
        print(variant.code())  # 19
    """

    def __init__(self):
        """Create a UintVariant instance."""
        self._code = 19  # VT_UI4

    def code(self):
        """
        Returns VT_UI4 (19) for 32-bit unsigned integer.

        Returns:
            int: 19
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "UInt32"
        """
        return "UInt32"


class Int16Variant(Variant):
    """
    16-bit signed integer variant type.

    Example usage:
        variant = Int16Variant()
        print(variant.code())  # 2
    """

    def __init__(self):
        """Create an Int16Variant instance."""
        self._code = 2  # VT_I2

    def code(self):
        """
        Returns VT_I2 (2) for 16-bit integer.

        Returns:
            int: 2
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "Int16"
        """
        return "Int16"


class Uint16Variant(Variant):
    """
    16-bit unsigned integer variant type.

    Example usage:
        variant = Uint16Variant()
        print(variant.code())  # 18
    """

    def __init__(self):
        """Create a Uint16Variant instance."""
        self._code = 18  # VT_UI2

    def code(self):
        """
        Returns VT_UI2 (18) for 16-bit unsigned integer.

        Returns:
            int: 18
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "UInt16"
        """
        return "UInt16"


class FloatVariant(Variant):
    """
    32-bit floating point variant type.

    Example usage:
        variant = FloatVariant()
        print(variant.code())  # 4
    """

    def __init__(self):
        """Create a FloatVariant instance."""
        self._code = 4  # VT_R4

    def code(self):
        """
        Returns VT_R4 (4) for 32-bit float.

        Returns:
            int: 4
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "Float"
        """
        return "Float"


class DoubleVariant(Variant):
    """
    64-bit floating point variant type.

    Example usage:
        variant = DoubleVariant()
        print(variant.code())  # 5
    """

    def __init__(self):
        """Create a DoubleVariant instance."""
        self._code = 5  # VT_R8

    def code(self):
        """
        Returns VT_R8 (5) for 64-bit double.

        Returns:
            int: 5
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "Double"
        """
        return "Double"


class StringVariant(Variant):
    """
    String variant type.

    Example usage:
        variant = StringVariant()
        print(variant.code())  # 8
    """

    def __init__(self):
        """Create a StringVariant instance."""
        self._code = 8  # VT_BSTR

    def code(self):
        """
        Returns VT_BSTR (8) for string.

        Returns:
            int: 8
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "String"
        """
        return "String"


class BoolVariant(Variant):
    """
    Boolean variant type.

    Example usage:
        variant = BoolVariant()
        print(variant.code())  # 11
    """

    def __init__(self):
        """Create a BoolVariant instance."""
        self._code = 11  # VT_BOOL

    def code(self):
        """
        Returns VT_BOOL (11) for boolean.

        Returns:
            int: 11
        """
        return self._code

    def name(self):
        """
        Returns type name.

        Returns:
            str: "Boolean"
        """
        return "Boolean"
