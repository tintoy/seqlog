#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_seqlog
----------------------------------

Tests for `seqlog` module.
"""

import logging
import pytest


from seqlog.structured_logging import StructuredLogRecord


class TestStructuredLogRecord(object):
    @classmethod
    def setup_class(cls):
        pass

    def test_named_arguments_message(self):
        record = StructuredLogRecord(
            name="name",
            level=logging.INFO,
            pathname="test.py",
            lineno=17,
            msg="Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}",
            args=None,
            exc_info=None,
            log_props={
                "Argument1": "Foo",
                "Argument2": "Bar",
                "Argument3": 7
            }
        )

        expected = "'Foo', Arg2 = 'Bar', Arg3 = 7"
        actual = record.getMessage()

        assert(
            expected == actual,
            "Unexpected log message: '{}'".format(actual)
        )

    def test_named_arguments_template(self):
        record = StructuredLogRecord(
            name="name",
            level=logging.INFO,
            pathname="test.py",
            lineno=17,
            msg="Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}",
            args=None,
            exc_info=None,
            log_props={
                "Argument1": "Foo",
                "Argument2": "Bar",
                "Argument3": 7
            }
        )

        expected = "Arg1 = '{Argument1}', Arg2 = '{Argument2}', Arg3 = {Argument3}"
        actual = record.msg

        assert (
            expected == actual,
            "Unexpected log message template: '{}'".format(actual)
        )

    @classmethod
    def teardown_class(cls):
        pass

