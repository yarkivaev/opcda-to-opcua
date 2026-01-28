# -*- coding: utf-8 -*-
"""
Logging configuration for the OPC bridge.

Log provides configured logging for the application
with appropriate formatting and handlers.

Example usage:
    logger = Log("opcda_bridge").logger()
    logger.info("Bridge started")
"""
import logging
import sys


class Log(object):
    """
    Logging configuration for the application.

    Log sets up a logger with console output and appropriate
    formatting for the OPC bridge application.

    Example usage:
        log = Log("opcda_bridge")
        logger = log.logger()
        logger.info("Message")
    """

    def __init__(self, name, level=logging.INFO):
        """
        Create Log with name and level.

        Args:
            name (str): Logger name
            level: Logging level (default INFO)
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def logger(self):
        """
        Extract configured logger.

        Returns:
            Logger: Configured logging.Logger instance
        """
        return self._logger
