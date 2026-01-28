# -*- coding: utf-8 -*-
"""
Marker objects for operation results.

These simple objects indicate operation states without
carrying additional data.

Example usage:
    def connect():
        if success:
            return Right(Connected())
        return Left(Problem("Connection failed", ""))
"""


class Connected(object):
    """
    Marker indicating successful connection.

    Example usage:
        result = Right(Connected())
    """

    def __init__(self):
        """Create Connected marker."""
        self._marker = True


class Disconnected(object):
    """
    Marker indicating successful disconnection.

    Example usage:
        result = Right(Disconnected())
    """

    def __init__(self):
        """Create Disconnected marker."""
        self._marker = True


class Success(object):
    """
    Marker indicating generic success.

    Example usage:
        result = Right(Success())
    """

    def __init__(self):
        """Create Success marker."""
        self._marker = True


class Running(object):
    """
    Marker indicating sync is running.

    Example usage:
        result = Right(Running())
    """

    def __init__(self):
        """Create Running marker."""
        self._marker = True


class Stopped(object):
    """
    Marker indicating sync is stopped.

    Example usage:
        result = Right(Stopped())
    """

    def __init__(self):
        """Create Stopped marker."""
        self._marker = True
