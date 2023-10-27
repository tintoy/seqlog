from logging import LogRecord
import seqlog
import tests.stubs
from seqlog.structured_logging import StructuredLogger


class DictConfigLogger(StructuredLogger):
    def __init__(self, name, level=seqlog.logging.NOTSET):
        super().__init__(name, level)

    def callHandlers(self, record: LogRecord) -> None:
        super().callHandlers(record)
        popped = False
        for handler in self.handlers:
            if isinstance(handler, tests.stubs.StubStructuredLogHandler):
                handler.pop_record()
                popped = True
        if not popped:
            raise Exception("Could not pop record from handler! No handler instance found for class 'StubStructuredLogHandler'.!")


TEST_CONFIG = {
    "version": 1,
    "loggers": {
        "test_logger": {
            "level": seqlog.logging.INFO,
            "handlers": ['test_handler'],
            "propagate": False,
            # "parent": "root",
            # "class": TestDictConfigLogger
        }
    },
    "handlers": {
        "test_handler": {
            "class": 'tests.stubs.StubStructuredLogHandler',
            "formatter": "test_formatter"
        }
    },
    "formatters": {
        "test_formatter": {
            "style": '{',
            "validate": True,
            "format": "[{levelname}] {asctime}: {name} (<{module}:{funcName}> {filename}:{lineno}) {msg}"
        }
    }
}


class TestDictConfig():
    def test_logger_with_dict_config(self):
        global TEST_CONFIG
        test_levels = {
            "critical": seqlog.logging.CRITICAL,
            "error": seqlog.logging.ERROR,
            "warning": seqlog.logging.WARNING,
            "info": seqlog.logging.INFO,
            "debug": seqlog.logging.DEBUG,
            "notset": seqlog.logging.NOTSET,
        }
        seqlog.logging.setLoggerClass(DictConfigLogger)

        for level in test_levels.keys():
            TEST_CONFIG['loggers']['test_logger']['level'] = test_levels.get(level)
            seqlog.configure_from_dict(TEST_CONFIG)

            for log_level in test_levels:
                test_logger = seqlog.logging.getLogger('test_logger')
                test_logger.log(msg=f"This is a {log_level} log sent with {level} set.", level=test_levels.get(level))
