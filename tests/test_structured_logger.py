#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_structured_logger
----------------------------------

Tests for `seqlog.structured_logging.StructuredLogger` class.
"""

import logging

import tests.assertions as expect

from seqlog import clear_global_log_properties
from seqlog.structured_logging import StructuredLogger
from tests.stubs import StubStructuredLogHandler


class TestStructuredLogger(object):

    def test_passing_none(self):
        logger, handler = create_logger()

        logger.info(None)

    def test_unjsonable(self):
        logger, handler = create_logger()

        class Test:
            pass

        logger.info('message %s', Test())
        handler.pop_record()

    def test_ordinal_arguments_message(self):
        logger, handler = create_logger()

        logger.info("Arg1 = '%s', Arg2 = '%s', Arg3 = %d", "Foo", "Bar", 7)

        record = handler.pop_record()
        expect.log_message(record, "Arg1 = 'Foo', Arg2 = 'Bar', Arg3 = 7")

    def test_ordinal_arguments_template(self):
        logger, handler = create_logger()

        logger.info("Arg1 = '%s', Arg2 = '%s', Arg3 = %d", "Foo", "Bar", 7)

        record = handler.pop_record()
        expect.log_template(record, "Arg1 = '%s', Arg2 = '%s', Arg3 = %d")

    def test_ordinal_arguments_level(self):
        logger, handler = create_logger(logging.WARNING)

        logger.warning("Arg1 = '%s', Arg2 = '%s', Arg3 = %d", "Foo", "Bar", 7)

        record = handler.pop_record()
        expect.log_level(record, logging.WARNING)

    def test_ordinal_arguments_args(self):
        logger, handler = create_logger()

        logger.info("Arg1 = '%s', Arg2 = '%s', Arg3 = %s, Arg4 = %d", "Foo", "Bar", b"Baz", 7)

        record = handler.pop_record()
        expect.log_ordinal_args(record, "Foo", "Bar", b"Baz", 7)

    def test_named_arguments_message(self):
        logger, handler = create_logger()

        logger.info(
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}, Arg4 = {Argument4}, Arg5 = {Argument5}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=b"Baz",
            Argument4=7,
            Argument5={"Key1": 1, "Array": [{"InArrayNum1": 111, "InArrayStr1": "str1"}]}
        )

        record = handler.pop_record()
        expect.log_message(record, "Arg1 = 'Foo', Arg2 = 'Bar', Arg3 = b'Baz', Arg4 = 7, "
                                   "Arg5 = {'Key1': 1, 'Array': [{'InArrayNum1': 111, 'InArrayStr1': 'str1'}]}")

    def test_named_arguments_template(self):
        logger, handler = create_logger()

        logger.info(
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}, Arg4 = {Argument4}, Arg5 = {Argument5}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=b"Baz",
            Argument4=7,
            Argument5={"Key1": 1, "Array": [{"InArrayNum1": 111, "InArrayStr1": "str1"}]}
        )

        record = handler.pop_record()
        expect.log_template(record,
                            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}, "
                            "Arg4 = {Argument4}, Arg5 = {Argument5}")

    def test_named_arguments_level(self):
        logger, handler = create_logger(logging.WARNING)

        logger.warning(
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}, Arg4 = {Argument4}, Arg5 = {Argument5}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=b"Baz",
            Argument4=7,
            Argument5={"Key1": 1, "Array": [{"InArrayNum1": 111, "InArrayStr1": "str1"}]}
        )

        record = handler.pop_record()
        expect.log_level(record, logging.WARNING)

    def test_named_arguments_args(self):
        logger, handler = create_logger()

        logger.info("Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}, "
                    "Arg4 = {Argument4}, Arg5 = {Argument5}",
                    Argument1="Foo",
                    Argument2="Bar",
                    Argument3=b"Baz",
                    Argument4=7,
                    Argument5={"Key1": 1, "Array": [{"InArrayNum1": 111, "InArrayStr1": "str1"}]})

        record = handler.pop_record()
        expect.log_named_args(record, Argument1="Foo", Argument2="Bar", Argument3=b"Baz", Argument4=7,
                              Argument5={"Key1": 1, "Array": [{"InArrayNum1": 111, "InArrayStr1": "str1"}]},
                              LoggerName="test")


def create_logger(level=logging.INFO):
    """
    Create a StructuredLogger and StubStructuredLogHandler for use in tests.
    :param level: The logger's initially-configured level.
    :return: The logger and handler.
    """

    clear_global_log_properties()
    logger = StructuredLogger("test", level)

    stub_handler = StubStructuredLogHandler()
    logger.addHandler(stub_handler)

    return logger, stub_handler
