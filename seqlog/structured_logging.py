# -*- coding: utf-8 -*-

import base64
import copy
import json
import importlib
import inspect
import logging
import os
import socket
import sys
import typing as tp
import warnings
from datetime import datetime
from dateutil.tz import tzlocal
from queue import Queue
import requests

from seqlog.consumer import QueueConsumer
from seqlog.feature_flags import FeatureFlag, is_feature_enabled

# Well-known keyword arguments used by the logging system.
_well_known_logger_kwargs = {"extra", "exc_info", "func", "sinfo"}

# Default global log properties.
_default_global_log_props = {
    "MachineName": socket.gethostname(),
    "ProcessId": os.getpid()
}

# Global properties attached to all log entries.
_global_log_props = _default_global_log_props
# Whether the _global_log_props DOES NOT contain any callables
_global_log_props_is_raw_dict = True
_callback_on_failure = None     # type: tp.Callable[[Exception], None]


def get_global_log_properties(logger_name=None):
    """
    Get the properties to be added to all structured log entries.

    :param logger_name: An optional logger name to be added to the log entry.
    :type logger_name: str
    :return: A copy of the global log properties.
    :rtype: dict
    """
    if _global_log_props_is_raw_dict:
        global_log_properties = copy.copy(_global_log_props)
    else:
        global_log_properties = {}
        for k, v in _global_log_props.items():
            if callable(v):
                v = v()
                if v is None:
                    continue
            global_log_properties[k] = v

    if logger_name:
        global_log_properties["LoggerName"] = logger_name

    return global_log_properties


def set_global_log_properties(**properties):
    """
    Configure the properties to be added to all structured log entries.

    :param properties: Keyword arguments representing the properties.
    :type properties: dict
    """

    global _global_log_props, _global_log_props_is_raw_dict
    _global_log_props_is_raw_dict = not any(callable(v) for v in properties.values())
    _global_log_props = copy.copy(properties)


def reset_global_log_properties():
    """
    Initialize global log properties to their default values.
    """

    global _global_log_props, _global_log_props_is_raw_dict
    _global_log_props_is_raw_dict = True
    _global_log_props = _default_global_log_props


def clear_global_log_properties():
    """
    Remove all global properties.
    """

    global _global_log_props, _global_log_props_is_raw_dict
    _global_log_props_is_raw_dict = True
    _global_log_props = {}


def set_callback_on_failure(callback):  # type: (tp.Callable[[Exception], None]) -> None
    """
    Configure a callback to be invoked each time logging fails.

    :param callback: A callable that takes an Exception (representing the logging failure) as its only argument.
    :type callback: callable
    """

    global _callback_on_failure
    assert callable(callback), 'Given callback is not callable'
    _callback_on_failure = callback


class StructuredLogRecord(logging.LogRecord):
    """
    An extended LogRecord that with custom properties to be logged to Seq.
    """

    def __init__(self, name, level, pathname, lineno, msg, args,
                 exc_info, func=None, sinfo=None, log_props=None, **kwargs):

        """
        Create a new StructuredLogRecord.
        :param name: The name of the logger that produced the log record.
        :param level: The logging level (severity) associated with the logging record.
        :param pathname: The name of the file (if known) where the log entry was created.
        :param lineno: The line number (if known) in the file where the log entry was created.
        :param msg: The log message (or message template).
        :param args: Ordinal message format arguments (if any).
        :param exc_info: Exception information to be included in the log entry.
        :param func: The function (if known) where the log entry was created.
        :param sinfo: Stack trace information (if known) for the log entry.
        :param log_props: Named message format arguments (if any).
        :param kwargs: Keyword (named) message format arguments.
        """

        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func, sinfo, **kwargs)

        self.log_props = log_props or {}

        if self.thread and "ThreadId" not in self.log_props:
            self.log_props["ThreadId"] = self.thread

        if self.threadName and "ThreadName" not in self.log_props:
            self.log_props["ThreadName"] = self.threadName

    def getMessage(self):
        """
        Get a formatted message representing the log record (with arguments replaced by values as appropriate).
        :return: The formatted message.
        """
        if self.msg is None:
            warnings.warn('You just passed a None as a message content!', UserWarning)
            self.msg = ''

        if self.args:
            return self.msg % self.args
        elif self.log_props:
            try:
                return self.msg.format(**self.log_props)
            except (KeyError, IndexError):
                # IndexError because sometimes the wrong log messages go like {existing_prop[0]}
                return self.msg   # handle the situation where we have braces in the logging value
        else:
            return self.msg


class StructuredLogger(logging.Logger):
    """
    Custom (dummy) logger that understands named log arguments.
    """

    def __init__(self, name, level=logging.NOTSET):
        """
        Create a new StructuredLogger
        :param name: The logger name.
        :param level: The logger minimum level (severity).
        """

        super().__init__(name, level)

        self._support_extra_properties = is_feature_enabled(FeatureFlag.EXTRA_PROPERTIES)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        """
        Called by public logger methods to generate a log entry.
        :param level: The level (severity) for the log entry.
        :param msg: The log message or message template.
        :param args: Ordinal arguments for the message format template.
        :param exc_info: Exception information to be included in the log entry.
        :param extra: Extra information to be included in the log entry.
        :param stack_info: Include stack-trace information in the log entry?
        :param kwargs: Keyword arguments (if any) passed to the public logger method that called _log.
        """

        # Slightly hacky:
        #
        # We take keyword arguments provided to public logger methods (except
        # well-known ones used by the logging system itself) and move them
        # into the `extra` argument as a sub-dictionary.

        # Start off with a copy of the global log properties.
        log_props = get_global_log_properties(self.name)

        # Add supplied keyword arguments.
        for prop in kwargs.keys():
            if prop in _well_known_logger_kwargs:
                continue

            log_props[prop] = kwargs[prop]

        if extra and self._support_extra_properties:
            for extra_prop in extra.keys():
                log_props['Extra_' + extra_prop] = extra[extra_prop]

        extra = extra or {}
        extra['log_props'] = log_props

        super()._log(level, msg, args, exc_info, extra, stack_info)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """
        Create a LogRecord.

        :param name: The name of the logger that produced the log record.
        :param level: The logging level (severity) associated with the logging record.
        :param fn: The name of the file (if known) where the log entry was created.
        :param lno: The line number (if known) in the file where the log entry was created.
        :param msg: The log message (or message template).
        :param args: Ordinal message format arguments (if any).
        :param exc_info: Exception information to be included in the log entry.
        :param func: The function (if known) where the log entry was created.
        :param extra: Extra information (if any) to add to the log record.
        :param sinfo: Stack trace information (if known) for the log entry.
        """

        # Do we have named format arguments?
        if extra and 'log_props' in extra:
            record = StructuredLogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo, extra['log_props'])
        else:
            record = super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

        if sinfo and not record.exc_text:
            setattr(record, 'exc_text', sinfo)

        return record


class StructuredRootLogger(logging.RootLogger):
    """
    Custom root logger that understands named log arguments.
    """

    def __init__(self, level=logging.NOTSET):
        """
        Create a `StructuredRootLogger`.
        """

        super().__init__(level)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        """
        Called by public logger methods to generate a log entry.

        :param level: The level (severity) for the log entry.
        :param msg: The log message or message template.
        :param args: Ordinal arguments for the message format template.
        :param exc_info: Exception information to be included in the log entry.
        :param extra: Extra information to be included in the log entry.
        :param stack_info: Include stack-trace information in the log entry?
        :param kwargs: Keyword arguments (if any) passed to the public logger method that called _log.
        """

        # Slightly hacky:
        #
        # We take keyword arguments provided to public logger methods (except
        # well-known ones used by the logging system itself) and move them
        # into the `extra` argument as a sub-dictionary.
        log_props = get_global_log_properties(self.name)
        for prop in kwargs.keys():
            if prop in _well_known_logger_kwargs:
                continue

            log_props[prop] = kwargs[prop]

        extra = extra or {}
        extra['log_props'] = log_props

        super()._log(level, msg, args, exc_info, extra, stack_info)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """
        Create a `LogRecord`.

        :param name: The name of the logger that produced the log record.
        :param level: The logging level (severity) associated with the logging record.
        :param fn: The name of the file (if known) where the log entry was created.
        :param lno: The line number (if known) in the file where the log entry was created.
        :param msg: The log message (or message template).
        :param args: Ordinal message format arguments (if any).
        :param exc_info: Exception information to be included in the log entry.
        :param func: The function (if known) where the log entry was created.
        :param extra: Extra information (if any) to add to the log record.
        :param sinfo: Stack trace information (if known) for the log entry.
        """

        # Do we have named format arguments?
        if extra and 'log_props' in extra:
            return StructuredLogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo, extra['log_props'])

        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)


class ConsoleStructuredLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        msg = self.format(record)

        print(msg)
        if hasattr(record, 'kwargs'):
            print("\tLog entry properties: {}".format(repr(record.kwargs)))


def best_effort_json_encode(arg):
    # No encoding necessary for strings.
    if isinstance(arg, str):
        return arg

    try:
        return json.dumps(arg)
    except TypeError:
        try:
            return str(arg)
        except TypeError:
            try:
                return repr(arg)
            except TypeError:
                return '<type %s>' % (type(arg), )
    except ReferenceError:
        return '<gone weak reference>'


class SeqLogHandler(logging.Handler):
    """
    Log handler that posts to Seq.
    """

    def __init__(self, server_url, api_key=None, batch_size=10, auto_flush_timeout=None, json_encoder_class=None):
        """
        Create a new `SeqLogHandler`.

        :param server_url: The Seq server URL.
        :param api_key: The Seq API key (if any).
        :param batch_size: The number of messages to batch up before posting to Seq.
        :param auto_flush_timeout: If specified, the time (in seconds) before
                                   the current batch is automatically flushed.
        :param json_encoder_class: The custom JSON encoder class (or fully-qualified class name), if any, to use.
        """

        super().__init__()

        self._support_stack_info = is_feature_enabled(FeatureFlag.STACK_INFO)

        self.server_url = server_url
        if not self.server_url.endswith("/"):
            self.server_url += "/"
        self.server_url += "api/events/raw"

        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"

        if api_key:
            self.session.headers["X-Seq-ApiKey"] = api_key

        json_encoder_class = json_encoder_class or json.encoder.JSONEncoder
        self.json_encoder_class = _ensure_class(json_encoder_class, compatible_class=json.encoder.JSONEncoder)

        self.log_queue = Queue()
        self.consumer = QueueConsumer(
            name="SeqLogHandler",
            queue=self.log_queue,
            callback=self.publish_log_batch,
            batch_size=batch_size,
            auto_flush_timeout=auto_flush_timeout
        )
        self.consumer.start()

    def flush(self):
        try:
            self.consumer.flush()
        finally:
            super().flush()

    def emit(self, record):
        """
        Emit a log record.

        :param record: The LogRecord.
        """

        self.log_queue.put(record, block=False)

    def close(self):
        """
        Close the log handler.
        """

        try:
            if self.consumer.is_running:
                self.consumer.stop()

            # TODO: Implement QueueConsumer.join() so we can wait
            # for processing to complete before closing the HTTP session

            # self.consumer.join()

            self.session.close()
        finally:
            super().close()

    def publish_log_batch(self, batch):     # type: (tp.Iterable[StructuredLogRecord]) -> None
        """
        Publish a batch of log records.

        :param batch: A list representing the batch.
        """

        if len(batch) == 0:
            return

        processed_records = []
        for record in batch:
            resp = self._build_event_data(record)
            try:
                resp = json.dumps(resp, cls=self.json_encoder_class)
            except TypeError:
                # cannot serialize to JSON
                # report an serialization error and continue serializing what you can
                self.handleError(record)
                continue
            processed_records.append(resp)

        request_body_json = '{"Events": [%s]}' % (','.join(processed_records), )

        self.acquire()
        response = None
        try:
            response = self.session.post(
                self.server_url,
                data=request_body_json,
                stream=True  # prevent '362'
            )
            response.raise_for_status()
        except requests.RequestException as requestFailed:
            # Only notify for the first record in the batch, or we'll be generating too much noise.
            self.handleError(batch[0])

            if _callback_on_failure is not None:
                _callback_on_failure(requestFailed)

            # Attempt to log error response
            if not requestFailed.response:
                sys.stderr.write('Response from Seq was unavailable.\n')
            elif not requestFailed.response.text:
                sys.stderr.write('Response body from Seq was empty.\n')
            else:
                sys.stderr.write('Response body from Seq:\n{0}\n'.format(
                    requestFailed.response.text
                ))
        finally:
            self.release()

    def _build_event_data(self, record):
        """
        Build an event data dictionary from the specified log record for submission to Seq.

        :param record: The LogRecord.
        :type record: StructuredLogRecord
        :return: A dictionary containing event data representing the log record.
        :rtype: dict
        """

        if record.args:
            # Standard (unnamed) format arguments (use 0-base index as property name).
            log_props_shim = get_global_log_properties(record.name)

            for (arg_index, arg) in enumerate(record.args or []):
                # bytes is not serialisable to JSON; encode appropriately.
                arg = _encode_bytes_if_required(arg)
                arg = best_effort_json_encode(arg)
                log_props_shim[str(arg_index)] = arg

            event_data = {
                "Timestamp": _get_local_timestamp(record),
                "Level": logging.getLevelName(record.levelno),
                "MessageTemplate": record.getMessage(),
                "Properties": log_props_shim
            }
        elif isinstance(record, StructuredLogRecord):
            # Named format arguments (and, therefore, log event properties).

            if record.log_props:
                for log_prop_name in record.log_props.keys():
                    # bytes is not serialisable to JSON; encode appropriately.
                    log_prop = record.log_props[log_prop_name]
                    arg = _encode_bytes_if_required(log_prop)
                    arg = best_effort_json_encode(arg)
                    record.log_props[log_prop_name] = arg

            event_data = {
                "Timestamp": _get_local_timestamp(record),
                "Level": logging.getLevelName(record.levelno),
                "MessageTemplate": record.msg,
                "Properties": record.log_props
            }
        else:
            # No format arguments; interpret message as-is.
            event_data = {
                "Timestamp": _get_local_timestamp(record),
                "Level": logging.getLevelName(record.levelno),
                "MessageTemplate": record.getMessage(),
                "Properties": get_global_log_properties()
            }

        if record.exc_text:
            # Rendered exception has already been cached
            event_data["Exception"] = record.exc_text
        elif self._support_stack_info and record.stack_info and not record.exc_info:
            # Feature flag is set: fall back to stack_info (sinfo) if exc_info is not present
            event_data["Exception"] = record.stack_info
        elif isinstance(record.exc_info, tuple):
            # Exception info is present
            if record.exc_info[0] is None and self._support_stack_info and record.stack_info:
                event_data["Exception"] = "{0}--NoExeption\n{1}".format(logging.getLevelName(record.levelno), record.stack_info)
            else:
                event_data["Exception"] = record.exc_text = self.formatter.formatException(record.exc_info)
        elif record.exc_info:
            # Exception info needs to be captured
            exc_info = sys.exc_info()
            if exc_info and exc_info[0] is not None:
                event_data["Exception"] = record.exc_text = self.formatter.formatException(record.exc_info)

        return event_data


def _get_local_timestamp(record):
    """
    Get the record's UTC timestamp as an ISO-formatted date / time string.

    :param record: The LogRecord.
    :type record: StructuredLogRecord
    :return: The ISO-formatted date / time string.
    :rtype: str
    """

    timestamp = datetime.fromtimestamp(
        timestamp=record.created,
        tz=tzlocal()
    )

    return timestamp.isoformat(sep=' ')


def _ensure_class(class_or_class_name, compatible_class=None):
    """
    Ensure that the supplied value is either a class or a fully-qualified class name.

    :param name: A class or a fully-qualified class name.
    :param expected_base_class: If specified then the class must be, or (eventually) derive from, this class.
    :return: The class represented by class_or_class_name.
    """

    target_class = class_or_class_name
    if isinstance(class_or_class_name, str):
        name_parts = class_or_class_name.split('.')
        module_name = '.'.join(
            name_parts[:-1]
        )
        target_class_name = name_parts[-1]

        # Raises ModuleNotFoundError if we can't resolve part of the module path
        target_module = importlib.import_module(module_name)

        target_class = getattr(target_module, target_class_name, None)
        if not target_class:
            raise ImportError("Class not found: '{}'.".format(class_or_class_name))

    if not inspect.isclass(target_class):
        raise TypeError(
            "'{}' is not a class.".format(class_or_class_name)
        )

    if compatible_class and not issubclass(target_class, compatible_class):
        raise ValueError(
            "Class '{}' does not derive from '{}.{}'.".format(
                class_or_class_name,
                compatible_class.__module__,
                compatible_class.__name__
            )
        )

    return target_class


def _encode_bytes_if_required(data):
    """
    If the specified data is represented as bytes, convert it to a UTF8 string (using Base64 encoding if the bytes do not represent valid UTF8).

    This is needed because json.dumps cannot serialise bytes.

    :param data: The data to encode.
    :return: If the data is represented as bytes, an equivalent UTF8 or Base64-encoded string; otherwise, the original data.
    """

    if (not isinstance(data, bytes)):
        return data

    try:
        data = data.decode('utf8')
    except UnicodeDecodeError:
        data = base64.encodebytes(data).decode('ascii')

    return data
