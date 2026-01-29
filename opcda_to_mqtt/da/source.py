# -*- coding: utf-8 -*-
"""
DaSource interface for OPC-DA tag discovery.

Example:
    >>> source = FakeDaSource([TagPath("Tag1"), TagPath("Tag2")])
    >>> result = source.discover("COM1")
    >>> result.is_right()
    True
"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod


class DaSource:
    """
    Interface for OPC-DA tag discovery.

    Implementations discover tags from OPC-DA servers.

    Example:
        >>> class MySource(DaSource):
        ...     def discover(self, prefix):
        ...         return Right([TagPath("Tag1")])
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def discover(self, prefix):
        """
        Discover all tags under the given prefix.

        Args:
            prefix: Tag path prefix to search under

        Returns:
            Either[Problem, list of TagPath]
        """
        raise NotImplementedError()
