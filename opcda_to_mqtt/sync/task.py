# -*- coding: utf-8 -*-
"""
Task interface and ReadTask implementation.

Example:
    >>> def callback(result):
    ...     print("Got:", result)
    >>> task = ReadTask(TagPath("Tag1"), callback)
    >>> task.execute(fake_client)
"""
from __future__ import print_function

from abc import ABCMeta, abstractmethod


class Task:
    """
    Interface for executable tasks.

    Tasks are executed by workers with an OPC client.

    Example:
        >>> class MyTask(Task):
        ...     def execute(self, client):
        ...         client.read("tag")
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, client):
        """
        Execute the task using the OPC client.

        Args:
            client: OpenOPC client instance
        """
        raise NotImplementedError()


class ReadTask(Task):
    """
    Task that reads a tag and invokes callback.

    Reads a tag from OPC server and passes result to callback.

    Example:
        >>> results = []
        >>> task = ReadTask(TagPath("Tag1"), lambda r: results.append(r))
        >>> task.execute(client)  # Reads tag and calls callback
    """

    def __init__(self, tag, callback):
        """
        Create a ReadTask.

        Args:
            tag: TagPath to read
            callback: Function to call with read result
        """
        self._tag = tag
        self._callback = callback

    def execute(self, client):
        """
        Read the tag and invoke callback.

        Args:
            client: OpenOPC client instance
        """
        result = client.read(self._tag.text(), sync=True)
        self._callback(result)

    def tag(self):
        """
        Get the tag path.

        Returns:
            The TagPath to read
        """
        return self._tag

    def __repr__(self):
        """
        Return string representation.

        Returns:
            String showing ReadTask and its tag
        """
        return "ReadTask(%r)" % self._tag
