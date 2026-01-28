# -*- coding: utf-8 -*-
"""
Either monad for null-free error handling.

Either represents a computation that may succeed (Right) or fail (Left).
This eliminates null references by forcing explicit handling of both cases.

Example usage:
    def divide(a, b):
        if b == 0:
            return Left(Problem("Division by zero", "denominator is zero"))
        return Right(a / b)

    result = divide(10, 2)
    if result.successful():
        print(result.value())  # 5.0

    result = divide(10, 0)
    if not result.successful():
        print(result.problem().message())  # Division by zero
"""
from abc import ABC, abstractmethod


class Either(ABC):
    """
    Abstract base for Either monad representing success or failure.

    Either forces explicit handling of both success and failure cases,
    eliminating null references from error handling code paths.

    Example usage:
        result = some_operation()
        if result.successful():
            data = result.value()
        else:
            error = result.problem()
    """

    @abstractmethod
    def successful(self):
        """
        Query whether this Either represents success.

        Returns:
            bool: True if Right (success), False if Left (failure)
        """
        pass

    @abstractmethod
    def value(self):
        """
        Extract the success value.

        Returns:
            object: The wrapped success value

        Raises:
            RuntimeError: If called on Left (failure)
        """
        pass

    @abstractmethod
    def problem(self):
        """
        Extract the failure value.

        Returns:
            Problem: The wrapped failure value

        Raises:
            RuntimeError: If called on Right (success)
        """
        pass

    @abstractmethod
    def map(self, func):
        """
        Transform the success value if present.

        Args:
            func: Function to apply to success value

        Returns:
            Either: Right with transformed value, or unchanged Left
        """
        pass

    @abstractmethod
    def flatmap(self, func):
        """
        Chain with another Either-returning function.

        Args:
            func: Function returning Either to chain

        Returns:
            Either: Result of chained function, or unchanged Left
        """
        pass


class Right(Either):
    """
    Successful result in an Either monad.

    Right wraps a success value and provides transformation operations.
    All operations preserve the success state.

    Example usage:
        success = Right(42)
        doubled = success.map(lambda x: x * 2)
        print(doubled.value())  # 84
    """

    def __init__(self, content):
        """
        Create a Right with the success value.

        Args:
            content: The success value to wrap
        """
        self._content = content

    def successful(self):
        """
        Returns True for Right instances.

        Returns:
            bool: Always True
        """
        return True

    def value(self):
        """
        Extract the success value.

        Returns:
            object: The wrapped success value
        """
        return self._content

    def problem(self):
        """
        Raises RuntimeError since Right has no problem.

        Raises:
            RuntimeError: Always, as Right represents success
        """
        raise RuntimeError("Cannot extract problem from successful Right")

    def map(self, func):
        """
        Apply func to content and wrap in new Right.

        Args:
            func: Function to apply to success value

        Returns:
            Right: New Right with transformed value
        """
        return Right(func(self._content))

    def flatmap(self, func):
        """
        Apply func which returns Either.

        Args:
            func: Function returning Either

        Returns:
            Either: Result of applying func to content
        """
        return func(self._content)


class Left(Either):
    """
    Failed result in an Either monad.

    Left wraps a failure value (Problem) and short-circuits all
    transformation operations, preserving the failure state.

    Example usage:
        failure = Left(Problem("Connection failed", "timeout"))
        mapped = failure.map(lambda x: x * 2)  # Still Left
        print(mapped.problem().message())  # Connection failed
    """

    def __init__(self, error):
        """
        Create a Left with the error value.

        Args:
            error: The Problem describing the failure
        """
        self._error = error

    def successful(self):
        """
        Returns False for Left instances.

        Returns:
            bool: Always False
        """
        return False

    def value(self):
        """
        Raises RuntimeError since Left has no value.

        Raises:
            RuntimeError: Always, as Left represents failure
        """
        raise RuntimeError("Cannot extract value from failed Left")

    def problem(self):
        """
        Extract the error value.

        Returns:
            Problem: The wrapped failure value
        """
        return self._error

    def map(self, func):
        """
        Returns self since Left cannot be mapped.

        Args:
            func: Ignored

        Returns:
            Left: Self unchanged
        """
        return self

    def flatmap(self, func):
        """
        Returns self since Left cannot be flatmapped.

        Args:
            func: Ignored

        Returns:
            Left: Self unchanged
        """
        return self


class Problem(object):
    """
    Immutable representation of a failure reason.

    Problem encapsulates an error message and optional context
    for debugging and error reporting purposes.

    Example usage:
        problem = Problem("Connection failed", "host=192.168.1.1 port=4840")
        print(problem.message())  # Connection failed
        print(problem.context())  # host=192.168.1.1 port=4840
    """

    def __init__(self, message, context=""):
        """
        Create a Problem with message and context.

        Args:
            message (str): Human-readable error message
            context (str): Additional debugging context
        """
        self._message = message
        self._context = context

    def message(self):
        """
        Extract the error message.

        Returns:
            str: Human-readable error message
        """
        return self._message

    def context(self):
        """
        Extract the debugging context.

        Returns:
            str: Additional debugging information
        """
        return self._context

    def __str__(self):
        """
        Format as string for logging.

        Returns:
            str: Message with context if present
        """
        if self._context:
            return "%s: %s" % (self._message, self._context)
        return self._message
