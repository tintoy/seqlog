# -*- coding: utf-8 -*-

import logging
import logging.config
import typing
import yaml

from seqlog.feature_flags import FeatureFlag, configure_feature
from seqlog.structured_logging import StructuredLogger, StructuredRootLogger, _override_root_logger
from seqlog.structured_logging import SeqLogHandler, ConsoleStructuredLogHandler
from seqlog.structured_logging import get_global_log_properties as _get_global_log_properties
from seqlog.structured_logging import set_global_log_properties as _set_global_log_properties
from seqlog.structured_logging import clear_global_log_properties as _clear_global_log_properties
from seqlog.structured_logging import reset_global_log_properties as _reset_global_log_properties
from seqlog.structured_logging import set_callback_on_failure as _set_callback_on_failure

__author__ = 'Adam Friedman'
__email__ = 'tintoy@tintoy.io'
__version__ = '0.5.0a1'


def configure_from_file(file_name):
    """
    Configure Seq logging using YAML-format configuration file.

    .. deprecated: 0.5.0
        Use logging.config.fileConfig(). Also, let it be known that Python uses different format natively (your file cannot be YAML)

    Uses `logging.config.dictConfig()`.
    """

    with open(file_name) as config_file:
        config = yaml.load(config_file, Loader=yaml.SafeLoader)

    configure_from_dict(config)


def configure_from_dict(config):
    """
    Configure Seq logging using a dictionary.

    Uses `logging.config.dictConfig()`.

    .. deprecated: 0.5.0
        Use logging.config.dictConfig() directly.

    Note that if you provide None to any of the default arguments, it just won't get changed (ie. it will stay the same).

    :param config: A dict containing the configuration.
    :type config: dict
    """
    logging.config.dictConfig(config)


def log_to_seq(server_url, api_key=None, level=logging.WARNING,
               batch_size=10, auto_flush_timeout=None,
               additional_handlers=None, override_root_logger=False,
               json_encoder_class=None, support_extra_properties=False,
               support_stack_info=False,
               ignore_seq_submission_errors=False,
               use_clef=False,
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
    :param json_encoder_class: The custom JSONEncoder class (if any) to use. It not specified, the default JSONEncoder will be used.
    :param support_extra_properties: Support passing of additional properties to log via the `extra` argument?
    :type support_extra_properties: bool
    :param support_stack_info: Support attaching of stack-trace information (if available) to log records?
    :type support_stack_info: bool
    :param ignore_seq_submission_errors: Ignore errors encountered while sending log records to Seq?
    :type ignore_seq_submission_errors: bool
    :param use_clef: use more modern format to send events to Seq
    :type use_clef: bool
    :return: The `SeqLogHandler` that sends events to Seq. Can be used to forcibly flush records to Seq.
    :rtype: SeqLogHandler
    """

    configure_feature(FeatureFlag.EXTRA_PROPERTIES, support_extra_properties)
    configure_feature(FeatureFlag.STACK_INFO, support_stack_info)
    configure_feature(FeatureFlag.IGNORE_SEQ_SUBMISSION_ERRORS, ignore_seq_submission_errors)
    configure_feature(FeatureFlag.USE_CLEF, use_clef)

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


def log_to_console(level=logging.WARNING, override_root_logger=False, support_extra_properties=False, support_stack_info=False, **kwargs):
    """
    Configure the logging system to send log entries to the console.

    Note that the root logger will not log to Seq by default.

    :param level: The minimum level at which to log.
    :param override_root_logger: Override the root logger, too?
                                 Note - this might cause problems if third-party components try to be clever
                                 when using the logging.XXX functions.
    :param support_extra_properties: Support passing of additional properties to log via the `extra` argument?
    :type support_extra_properties: bool
    :param support_stack_info: Support attaching of stack-trace information (if available) to log records?
    :type support_stack_info: bool
    """

    configure_feature(FeatureFlag.EXTRA_PROPERTIES, support_extra_properties)
    configure_feature(FeatureFlag.STACK_INFO, support_stack_info)

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


def set_callback_on_failure(callback):  # type: (typing.Callable[[Exception], None]) -> None
    """
    Configure a callback to be invoked each time logging fails.

    :param callback: A callable that takes an Exception (representing the logging failure) as its only argument.
    :type callback: callable
    """

    _set_callback_on_failure(callback)


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
    :type properties: str
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

