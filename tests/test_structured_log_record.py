#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_structured_log_record
----------------------------------

Tests for `seqlog.structured_logging.StructuredLogRecord` class.
"""

import logging


from seqlog.structured_logging import StructuredLogRecord
import tests.assertions as expect

# Turn off thread-related logging, since it would interfere with these tests.
logging.threading = False


class TestStructuredLogRecord(object):
    #
    # Named arguments
    #

    def test_named_arguments_message(self):
        record = self.create_test_log_record(
            logging.INFO,
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=7
        )

        expect.log_message(record, "Arg1 = 'Foo', Arg2 = 'Bar', Arg3 = 7")

    def test_named_arguments_template(self):
        record = self.create_test_log_record(
            logging.INFO,
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=7
        )

        expect.log_template(record, "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}")

    def test_named_arguments_level(self):
        record = self.create_test_log_record(
            logging.WARNING,
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=7
        )

        expect.log_level(record, logging.WARNING)

    def test_named_arguments_args(self):
        record = self.create_test_log_record(
            logging.WARNING,
            "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}",
            Argument1="Foo",
            Argument2="Bar",
            Argument3=7
        )

        expect.log_named_args(record, Argument1="Foo", Argument2="Bar", Argument3=7)

    #
    # Ordinal arguments
    #

    def test_ordinal_arguments_message(self):
        record = self.create_test_log_record(
            logging.INFO,
            "Arg1 = '%s', Arg2 = '%s', Arg3 = %d",
            "Foo",
            "Bar",
            7
        )

        expect.log_message(record, "Arg1 = 'Foo', Arg2 = 'Bar', Arg3 = 7")

    def test_ordinal_arguments_template(self):
        record = self.create_test_log_record(
            logging.INFO,
            "Arg1 = '%s', Arg2 = '%s', Arg3 = %d",
            "Foo",
            "Bar",
            7
        )

        expect.log_template(record, "Arg1 = '%s', Arg2 = '%s', Arg3 = %d")

    def test_ordinal_arguments_level(self):
        record = self.create_test_log_record(
            logging.WARNING,
            "Arg1 = '%s', Arg2 = '%s', Arg3 = %d",
            "Foo",
            "Bar",
            7
        )

        expect.log_level(record, logging.WARNING)

    def test_ordinal_arguments_args(self):
        record = self.create_test_log_record(
            logging.INFO,
            "Arg1 = '%s', Arg2 = '%s', Arg3 = %d",
            "Foo",
            "Bar",
            7
        )

        expect.log_ordinal_args(record, "Foo", "Bar", 7)

    @staticmethod
    def create_test_log_record(level, message, *ordinal_args, **named_args):
        return StructuredLogRecord(
            name="DummyLogger",
            level=level,
            pathname="test.py",
            lineno=17,
            msg=message,
            args=ordinal_args,
            exc_info=None,
            log_props=named_args
        )
