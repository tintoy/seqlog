# -*- coding: utf-8 -*-

import datetime
import logging
import requests

# Well-known keyword arguments used by the logging system.
_well_known_logger_kwargs = [
    "extra",
    "exc_info",
    "func",
    "sinfo"
]


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

    def getMessage(self):
        """
        Get a formatted message representing the log record (with arguments replaced by values as appropriate).
        :return: The formatted message.
        """

        if self.args:
            return self.msg % self.args
        elif self.log_props:
            return self.msg.format(**self.log_props)
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
        log_props = {}
        for prop in kwargs.keys():
            if prop in _well_known_logger_kwargs:
                continue

            log_props[prop] = kwargs[prop]

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


class SeqLogHandler(logging.Handler):
    """
    Log handler that posts to Seq.

    TODO: Implement periodic (batched) posting.
    """

    def __init__(self, server_url, api_key=None):
        super().__init__()

        self.server_url = server_url
        if not self.server_url.ends_with("/"):
            self.server_url += "/"
        self.server_url += "api/events/raw"

        self.session = requests.Session()
        if api_key:
            self.session.headers["X-Seq-ApiKey"] = api_key

    def emit(self, record):
        if isinstance(record, StructuredLogRecord):
            # Named format arguments (and, therefore, log event properties).
            request_body = {
                "Events": [{
                    "Timestamp": datetime.datetime.now().isoformat(),
                    "Level": logging.getLevelName(record.level),
                    "MessageTemplate": record.msg,
                    "Properties": record.log_props
                }]
            }
        elif record.args:
            # Standard (unnamed) format arguments (use 0-base index as property name).
            log_props_shim = {}
            for (arg_index, arg) in enumerate(record.args or []):
                log_props_shim[str(arg_index)] = arg

            request_body = {
                "Events": [{
                    "Timestamp": datetime.datetime.now().isoformat(),
                    "Level": logging.getLevelName(record.level),
                    "MessageTemplate": record.getMessage(),
                    "Properties": log_props_shim
                }]
            }
        else:
            # No format arguments; interpret message as-is.
            request_body = {
                "Events": [{
                    "Timestamp": datetime.datetime.now().isoformat(),
                    "Level": logging.getLevelName(record.level),
                    "MessageTemplate": record.getMessage()
                }]
            }

        response = self.session.post(self.server_url, json=request_body)
        response.raise_for_status()

    def close(self):
        try:
            self.session.close()
        finally:
            super().close()
