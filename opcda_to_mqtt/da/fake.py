# -*- coding: utf-8 -*-
"""
FakeDaSource for testing.

Example:
    >>> source = FakeDaSource([TagPath("Tag1"), TagPath("Tag2")])
    >>> result = source.discover("")
    >>> len(result.fold(lambda e: [], lambda tags: tags))
    2
"""
from __future__ import print_function

from opcda_to_mqtt.da.source import DaSource
from opcda_to_mqtt.result.either import Right


class FakeDaSource(DaSource):
    """
    Test double for DaSource.

    Returns predefined tags for any discovery request.

    Example:
        >>> source = FakeDaSource([TagPath("A"), TagPath("B")])
        >>> source.discover("prefix").is_right()
        True
    """

    def __init__(self, tags):
        """
        Create a FakeDaSource with predefined tags.

        Args:
            tags: List of TagPath objects to return
        """
        self._tags = list(tags)

    def discover(self, prefix):
        """
        Return predefined tags regardless of prefix.

        Args:
            prefix: Tag path prefix (ignored)

        Returns:
            Right containing the predefined tags
        """
        return Right(list(self._tags))

    def tags(self):
        """
        Get the configured tags.

        Returns:
            List of TagPath objects
        """
        return list(self._tags)
