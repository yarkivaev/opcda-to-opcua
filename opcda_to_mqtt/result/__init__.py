# -*- coding: utf-8 -*-
"""
Result types for null-free design.

Provides Either and Optional ADTs for safe error handling.
"""
from __future__ import print_function

from opcda_to_mqtt.result.either import Either, Right, Left, Problem
from opcda_to_mqtt.result.optional import Optional, Some, Empty

__all__ = ['Either', 'Right', 'Left', 'Problem', 'Optional', 'Some', 'Empty']
