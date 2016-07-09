# -*- coding: utf-8 -*-

import dateutil.tz
import logging

from seqlog.structured_logging import StructuredLogRecord, StructuredLogger, StructuredRootLogger
from seqlog.structured_logging import SeqLogHandler, ConsoleStructuredLogHandler

__author__ = 'Adam Friedman'
__email__ = 'tintoy@tintoy.io'
__version__ = '0.0.1'

# TODO: Enable a dictionary of extra properties to be added to each outgoing message.
# TODO: Need to decide on the right mechanism for this.


def log_to_seq(server_url, api_key=None, level=logging.WARNING,
               batch_size=10, auto_flush_timeout=None, override_root_logger=False, **kwargs):
    """
    Configure the logging system to send log entries to Seq.

    Note that the root logger will not log to Seq by default (as this could interfere with the
    :param server_url: The Seq server URL.
    :param api_key: The Seq API key (optional).
    :param level: The minimum level at which to log.
    :param batch_size: The number of log entries to collect before publishing to Seq.
    :param auto_flush_timeout: If specified, the time (in milliseconds) before
    the current batch is automatically flushed.
    :param override_root_logger: Override the root logger, too?
    Note - this might cause problems if third-party components try to be clever when using the logging.XXX functions.
    :return: The `SeqLogHandler` that sends events to Seq. Can be used to forcibly flush records to Seq.
    :rtype: SeqLogHandler
    """

    logging.setLoggerClass(StructuredLogger)

    if override_root_logger:
        _override_root_logger()

    log_handler = SeqLogHandler(server_url, api_key, batch_size, auto_flush_timeout)
    logging.basicConfig(
        style='{',
        handlers=[log_handler],
        level=level,
        **kwargs
    )

    return log_handler


def log_to_console(level=logging.WARNING, override_root_logger=False, **kwargs):
    """
    Configure the logging system to send log entries to the console.

    Note that the root logger will not log to Seq by default (as this could interfere with the
    :param level: The minimum level at which to log.
    :param override_root_logger: Override the root logger, too?
    Note - this might cause problems if third-party components try to be clever when using the logging.XXX functions.
    """

    logging.setLoggerClass(StructuredLogger)

    if override_root_logger:
        _override_root_logger()

    logging.basicConfig(
        style='{',
        handlers=[
            ConsoleStructuredLogHandler()
        ],
        level=level,
        **kwargs
    )


def _override_root_logger():
    """
    Override the root logger with a `StructuredRootLogger`.
    """

    logging.root = StructuredRootLogger(logging.WARNING)
    logging.Logger.root = logging.root
    logging.Logger.manager = logging.Manager(logging.Logger.root)
