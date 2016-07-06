#!/usr/bin/env python3

import datetime
import logging
import requests


class StructuredLogRecord(logging.LogRecord):
    def __init__(self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None, log_props=None, **kwargs):
        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func, sinfo, **kwargs)

        self.log_props = log_props or {}

    def getMessage(self):
        if self.args:
            return self.msg % self.args
        elif self.log_props:
            return self.msg.format(**self.log_props)
        else:
            return self.msg


class StructuredLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
        log_props = {}
        for prop in kwargs.keys():
            if prop == "extra" or prop == "exc_info":
                continue

            log_props[prop] = kwargs[prop]

        extra = extra or {}
        extra['log_props'] = log_props
        super()._log(level, msg, args, exc_info, extra, stack_info)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        if extra and 'log_props' in extra:
            return StructuredLogRecord(name, level, fn, lno, msg, args, exc_info, func, sinfo, extra['log_props'])

        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)


class StructuredLogHandler(logging.Handler):
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

    def __init__(self, server_url, api_key):
        super().__init__()

        self.server_url = server_url + "/api/events/raw"
        self.api_key = api_key
        self.session = requests.Session()
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


logging.setLoggerClass(StructuredLogger)
logging.basicConfig(
    style='{',
    handlers=[StructuredLogHandler()],
    level=logging.INFO
)

logger1 = logging.getLogger("A")
logger1.info("Hello, {name}!", name="world")

logger2 = logging.getLogger("A.B")
logger2.info("Goodbye, {name}!", name="moon")

logging.info("Hello, %s.", "root logger")

logger3 = logging.getLogger("C")
logger3.info("Goodbye, %s!", "moon")
