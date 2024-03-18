# -*- coding: utf-8 -*-

import logging
import logging.config
import typing
import yaml

from seqlog.feature_flags import FeatureFlag, configure_feature
from seqlog.structured_logging import StructuredLogger, StructuredRootLogger
from seqlog.structured_logging import SeqLogHandler, ConsoleStructuredLogHandler
from seqlog.structured_logging import get_global_log_properties as _get_global_log_properties
from seqlog.structured_logging import set_global_log_properties as _set_global_log_properties
from seqlog.structured_logging import clear_global_log_properties as _clear_global_log_properties
from seqlog.structured_logging import reset_global_log_properties as _reset_global_log_properties
from seqlog.structured_logging import set_callback_on_failure as _set_callback_on_failure

__author__ = 'Adam Friedman'
__email__ = 'tintoy@tintoy.io'
__version__ = '0.3.30'


def configure_from_file(file_name, override_root_logger=True, support_extra_properties=False, support_stack_info=False, ignore_seq_submission_errors=False):
    """
    Configure Seq logging using YAML-format configuration file.

    Uses `logging.config.dictConfig()`.

    :param file_name: The name of the configuration file to use.
    :type file_name: str
    :param override_root_logger: Override the root logger to use a Seq-specific implementation? (default: True)
    :type override_root_logger: bool
    :param support_extra_properties: Support passing of additional properties to log via the `extra` argument?
    :type support_extra_properties: bool
    :param support_stack_info: Support attaching of stack-trace information (if available) to log records?
    :type support_stack_info: bool
    :param ignore_seq_submission_errors: Ignore errors encountered while sending log records to Seq?
    :type ignore_seq_submission_errors: bool
    """

    configure_feature(FeatureFlag.EXTRA_PROPERTIES, support_extra_properties)
    configure_feature(FeatureFlag.STACK_INFO, support_stack_info)
    configure_feature(FeatureFlag.IGNORE_SEQ_SUBMISSION_ERRORS, ignore_seq_submission_errors)

    with open(file_name) as config_file:
        config = yaml.load(config_file, Loader=yaml.SafeLoader)

    configure_from_dict(config, override_root_logger)


def configure_from_dict(config, override_root_logger=True, use_structured_logger=True, support_extra_properties=False, support_stack_info=False, ignore_seq_submission_errors=False):
    """
    Configure Seq logging using a dictionary.

    Uses `logging.config.dictConfig()`.

    :param config: A dict containing the configuration.
    :type config: dict
    :param override_root_logger: Override the root logger to use a Seq-specific implementation? (default: True)
    :type override_root_logger: bool
    :param use_structured_logger: Configure the default logger class to be StructuredLogger, which support named format arguments? (default: True)
    :type use_structured_logger: bool
    :param support_extra_properties: Support passing of additional properties to log via the `extra` argument?
    :type support_extra_properties: bool
    :param support_stack_info: Support attaching of stack-trace information (if available) to log records?
    :type support_stack_info: bool
    :param ignore_seq_submission_errors: Ignore errors encountered while sending log records to Seq?
    :type ignore_seq_submission_errors: bool
    """

    configure_feature(FeatureFlag.EXTRA_PROPERTIES, support_extra_properties)
    configure_feature(FeatureFlag.STACK_INFO, support_stack_info)
    configure_feature(FeatureFlag.IGNORE_SEQ_SUBMISSION_ERRORS, ignore_seq_submission_errors)

    if override_root_logger:
        _override_root_logger()

    # Must use StructuredLogger to support named format argments.
    if use_structured_logger:
        logging.setLoggerClass(StructuredLogger)

    logging.config.dictConfig(config)


def log_to_seq(server_url, api_key=None, level=logging.WARNING,
               name='DefaultSeqLogger', batch_size=10, auto_flush_timeout=None,
               additional_handlers=None, override_root_logger=False,
               json_encoder_class=None, support_extra_properties=False,
               support_stack_info=False,  handler=None, formatter=None,
               ignore_seq_submission_errors=False,
               **kwargs):
    """
    Configure the logging system to send log entries to Seq.

    Note that the root logger will not log to Seq by default.

    :param server_url: The Seq server URL.
    :param api_key: The Seq API key (optional).
    :param level: The minimum level at which to log.
    :param name: A name for the logger.
        if not specified, the name 'DefaultSeqLogger' will be used.
    :param batch_size: The number of log entries to collect before publishing to Seq.
    :param auto_flush_timeout: If specified, the time (in seconds) before the current batch is automatically flushed.
    :param additional_handlers: Additional `LogHandler`s (if any).
    :param override_root_logger: Override the root logger, too?
                                 Note - this might cause problems if third-party components try to be clever
                                 when using the logging.XXX functions.
    :param json_encoder_class: The custom JSONEncoder class (if any) to use.
        If not specified, the default JSONEncoder will be used.
    :param support_extra_properties: Support passing of additional properties to log via the `extra` argument?
    :type support_extra_properties: bool
    :param support_stack_info: Support attaching of stack-trace information (if available) to log records?
    :type support_stack_info: bool
    :param ignore_seq_submission_errors: Ignore errors encountered while sending log records to Seq?
    :type ignore_seq_submission_errors: bool
    :param handler: a custom/user-provided handler class for the StructuredLogger class
        If not specified, SeqLogHandler will be initialized and used.
    :type logging.Handler(class)
    :param formatter: a custom/user-provided formatter class for the SeqLogHandler() class.
        If not specified, `logging.Formatter(class)` will be initialized and used with a default format an style.
    :type: logging.Formatter(class)
    :return: The `StructuredLogger` so that the user can immediately start logging either with the return class, or with the `logging.log()` functions.
    :rtype: StructuredLogger(class)
    """

    configure_feature(FeatureFlag.EXTRA_PROPERTIES, support_extra_properties)
    configure_feature(FeatureFlag.STACK_INFO, support_stack_info)
    configure_feature(FeatureFlag.IGNORE_SEQ_SUBMISSION_ERRORS, ignore_seq_submission_errors)

    logging.setLoggerClass(StructuredLogger)

    if override_root_logger:
        _override_root_logger()

    if handler == None:
        seq_log_handler = SeqLogHandler(server_url, api_key, batch_size, auto_flush_timeout, json_encoder_class)
    else:
        seq_log_handler = handler

    if formatter == None:
        formatter = logging.Formatter(fmt='{asctime} - {message}', style='{')

    seq_log_handler.setFormatter(formatter)

    structured_logger = StructuredLogger(name=name, level=level)

    structured_logger.addHandler(seq_log_handler)

    if additional_handlers:
        for additional_handler in additional_handlers:
            structured_logger.addHandler(additional_handler)

    return structured_logger


def log_to_console(level=logging.WARNING, name='DefaultSeqConsoleLogger',
                   override_root_logger=False, support_extra_properties=False,
                   support_stack_info=False,
                   handler=ConsoleStructuredLogHandler(), formatter=None,
):
    """
    Configure the logging system to send log entries to the console.

    Note that the root logger will not log to Seq by default.

    :param level: The minimum level at which to log.
    :param name: a name for the console logger.
        If not specified, the name 'DefaultSeqConsoleLogger' will be used.
    :param override_root_logger: Override the root logger, too?
                                 Note - this might cause problems if third-party components try to be clever
                                 when using the logging.XXX functions.
    :param support_extra_properties: Support passing of additional properties to log via the `extra` argument?
    :type support_extra_properties: bool
    :param support_stack_info: Support attaching of stack-trace information (if available) to log records?
    :type support_stack_info: bool
    :param handler: the Handler class to use for the console logger.
        if not specified, `ConsoleStructuredLogHandler(class)` will be used.
    :param formatter: a Formatter class for the Handler to format logs with.
        if not specified, `logging.Formatter(class)` will be used with a default format and style.
    """

    configure_feature(FeatureFlag.EXTRA_PROPERTIES, support_extra_properties)
    configure_feature(FeatureFlag.STACK_INFO, support_stack_info)

    if override_root_logger:
        _override_root_logger()

    if formatter == None:
        formatter = logging.Formatter(fmt='{asctime} - {message}', style='{')

    handler.setFormatter(formatter)

    console_logger = StructuredLogger(name=name, level=level)

    console_logger.addHandler(handler)

    return console_logger


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


def _override_root_logger():
    """
    Override the root logger with a `StructuredRootLogger`.
    """

    logging.root = StructuredRootLogger(logging.WARNING)
    logging.Logger.root = logging.root
    logging.Logger.manager = logging.Manager(logging.Logger.root)
