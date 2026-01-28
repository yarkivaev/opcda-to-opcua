# -*- coding: utf-8 -*-
"""
Result types for null-free error handling.

This module provides Either and Optional algebraic data types
that eliminate null references from the codebase.
"""
from opcda_to_opcua.result.either import Either, Right, Left
from opcda_to_opcua.result.optional import Optional, Some, Empty
