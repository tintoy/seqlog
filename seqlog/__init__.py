# -*- coding: utf-8 -*-

import logging
import logging.config
import yaml

from seqlog.structured_logging import StructuredLogger, StructuredRootLogger
from seqlog.structured_logging import SeqLogHandler, ConsoleStructuredLogHandler
from seqlog.structured_logging import get_global_log_properties as _get_global_log_properties
from seqlog.structured_logging import set_global_log_properties as _set_global_log_properties
from seqlog.structured_logging import clear_global_log_properties as _clear_global_log_properties
from seqlog.structured_logging import reset_global_log_properties as _reset_global_log_properties

__author__ = 'Adam Friedman'
__email__ = 'tintoy@tintoy.io'
__version__ = '0.3.11'


def configure_from_file(file_name, override_root_logger=True, use_structured_logger=True):
    """
    Configure Seq logging using YAML-format configuration file.

    Uses `logging.config.dictConfig()`.

    :param file_name: The name of the configuration file to use.
    :type file_name: str
    :param override_root_logger: Override the root logger to use a Seq-specific implementation? (default: True)
    :param use_structured_logger: Configure the default logger class to be StructuredLogger, which support named format arguments? (default: True)
    :type override_root_logger: bool
    """

    with open(file_name) as config_file:
        config = yaml.load(config_file)

    configure_from_dict(config, override_root_logger)


def configure_from_dict(config, override_root_logger=True, use_structured_logger=True):
    """
    Configure Seq logging using a dictionary.

    Uses `logging.config.dictConfig()`.

    :param config: A dict containing the configuration.
    :type config: dict
    :param override_root_logger: Override the root logger to use a Seq-specific implementation? (default: True)
    :param use_structured_logger: Configure the default logger class to be StructuredLogger, which support named format arguments? (default: True)
    :type override_root_logger: bool
    """

    if override_root_logger:
        _override_root_logger()

    # Must use StructuredLogger to support named format argments.
    if use_structured_logger:
        logging.setLoggerClass(StructuredLogger)

    logging.config.dictConfig(config)


def log_to_seq(server_url, api_key=None, level=logging.WARNING,
               batch_size=10, auto_flush_timeout=None,
               additional_handlers=None, override_root_logger=False,
               json_encoder_class=None,
               **kwargs):
    """
    Configure the logging system to send log entries to Seq.

    Note that the root logger will not log to Seq by default.

    :param server_url: The Seq server URL.
    :param api_key: The Seq API key (optional).
    :param level: The minimum level at which to log.
    :param batch_size: The number of log entries to collect before publishing to Seq.
    :param auto_flush_timeout: If specified, the time (in seconds) before the current batch is automatically flushed.
    :param additional_handlers: Additional `LogHandler`s (if any).
    :param override_root_logger: Override the root logger, too?
                                 Note - this might cause problems if third-party components try to be clever
                                 when using the logging.XXX functions.
    :json_encoder_class: The custom JSONEncoder class (if any) to use. It not specified, the default JSONEncoder will be used.
    :return: The `SeqLogHandler` that sends events to Seq. Can be used to forcibly flush records to Seq.
    :rtype: SeqLogHandler
    """

    logging.setLoggerClass(StructuredLogger)

    if override_root_logger:
        _override_root_logger()

    log_handlers = [
        SeqLogHandler(server_url, api_key, batch_size, auto_flush_timeout, json_encoder_class)
    ]

    if additional_handlers:
        for additional_handler in additional_handlers:
            log_handlers.append(additional_handler)

    logging.basicConfig(
        style='{',
        handlers=log_handlers,
        level=level,
        **kwargs
    )

    return log_handlers[0]


def log_to_console(level=logging.WARNING, override_root_logger=False, **kwargs):
    """
    Configure the logging system to send log entries to the console.

    Note that the root logger will not log to Seq by default.

    :param level: The minimum level at which to log.
    :param override_root_logger: Override the root logger, too?
                                 Note - this might cause problems if third-party components try to be clever
                                 when using the logging.XXX functions.
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


def get_global_log_properties():
    """
    Get the properties to be added to all structured log entries.

    :return: A copy of the global log properties.
    :rtype: dict
    """

    return _get_global_log_properties()


def set_global_log_properties(**properties):
    """
    Configure the properties to be added to all structured log entries.

    :param properties: Keyword arguments representing the properties.
    :type properties: dict
    """

    _set_global_log_properties(**properties)


def reset_global_log_properties():
    """
    Initialize global log properties to their default values.
    """

    _reset_global_log_properties()


def clear_global_log_properties():
    """
    Remove all global properties.
    """

    _clear_global_log_properties()


def _override_root_logger():
    """
    Override the root logger with a `StructuredRootLogger`.
    """

    logging.root = StructuredRootLogger(logging.WARNING)
    logging.Logger.root = logging.root
    logging.Logger.manager = logging.Manager(logging.Logger.root)
