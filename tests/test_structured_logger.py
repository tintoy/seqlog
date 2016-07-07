#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_seqlog
----------------------------------

Tests for `seqlog` module.
"""

import logging
import pytest

from seqlog.structured_logging import StructuredLogger
from tests.assertions import *
from tests.stubs import StubStructuredLogHandler


class TestStructuredLogger(object):
    def test_ordinal_arguments_message(self):
        logger, handler = create_logger()

        logger.info("Arg1 = '%s', Arg2 = '%s', Arg3 = %d", "Foo", "Bar", 7)

        record = handler.pop_record()

        expect_log_message(record, "'Foo', Arg2 = 'Bar', Arg3 = 7")
        expect_log_level(record, logging.INFO)
        expect_log_ordinal_args(record, "Foo", "Bar", 7)

    def test_named_arguments_message(self):
        logger, handler = create_logger()

        logger.info(
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=7
        )

        record = handler.pop_record()

        expect_log_message(record, "'Foo', Arg2 = 'Bar', Arg3 = 7")
        expect_log_level(record, logging.INFO)
        expect_log_named_args(record, Argument1="Foo", Argument2="Bar", Argument3=7)


@pytest.fixture(scope="session")
def create_logger(level=logging.INFO):
    """
    Create a StructuredLogger and StubStructuredLogHandler for use in tests.
    :param level: The logger's initially-configured level.
    :return: The logger and handler.
    """

    logger = StructuredLogger("test", level)

    stub_handler = StubStructuredLogHandler()
    logger.addHandler(stub_handler)

    return logger, stub_handler

