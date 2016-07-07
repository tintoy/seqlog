# -*- coding: utf-8 -*-

import logging

from .structured_logging import StructuredLogRecord, StructuredLogger, SeqLogHandler, ConsoleStructuredLogHandler

__author__ = 'Adam Friedman'
__email__ = 'tintoy@tintoy.io'
__version__ = '0.0.1'


def log_to_seq(server_url, api_key=None, level=logging.WARNING, override_root_logger=False, **kwargs):
    """
    Configure the logging system to send log entries to Seq.

    Note that the root logger will not log to Seq by default (as this could interfere with the
    :param server_url: The Seq server URL.
    :param api_key: The Seq API key (optional).
    :param level: The minimum level at which to log.
    :param override_root_logger: Override the root logger, too?
    Note - this might cause problems if third-party components try to be clever when using the logging.XXX functions.
    """

    logging.setLoggerClass(StructuredLogger)
    logging.basicConfig(
        style='{',
        handlers=[
            SeqLogHandler(server_url, api_key)
        ],
        level=level,
        **kwargs
    )
    if override_root_logger:
        logging.root = StructuredLogger("root", level)


def log_to_console(level=logging.WARNING, override_root_logger=False, **kwargs):
    """
    Configure the logging system to send log entries to the console.

    Note that the root logger will not log to Seq by default (as this could interfere with the
    :param level: The minimum level at which to log.
    :param override_root_logger: Override the root logger, too?
    Note - this might cause problems if third-party components try to be clever when using the logging.XXX functions.
    """

    logging.setLoggerClass(StructuredLogger)
    logging.basicConfig(
        style='{',
        handlers=[
            ConsoleStructuredLogHandler()
        ],
        level=level,
        **kwargs
    )
    if override_root_logger:
        logging.root = StructuredLogger("root", level)
