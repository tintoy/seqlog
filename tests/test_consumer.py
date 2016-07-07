#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_seqlog
----------------------------------

Tests for `seqlog.consumer.LogRecordConsumer` module.
"""

import logging
from queue import Queue
from threading import Event

from seqlog.structured_logging import StructuredLogRecord
from seqlog.consumer import LogRecordConsumer
import tests.assertions as expect


class TestLogRecordConsumer(object):
    def test_batchsize_2_pre_fill(self):
        record_queue = Queue()
        record_queue.put("Item1")
        record_queue.put("Item2")

        batch_received = Event()

        def handler(record_batch):
            assert(
                len(record_batch) == 2,
                "Incorrect batch size (expected 2, but found {}.".format(
                    len(record_batch)
                )
            )

            batch_received.set()

        consumer = LogRecordConsumer(record_queue, handler, batch_size=2)
        consumer.start()

        batch_received.wait(timeout=2000)

        consumer.stop()

    def test_batchsize_2_post_fill(self):
        record_queue = Queue()

        batch_received = Event()

        def handler(record_batch):
            assert (
                len(record_batch) == 2,
                "Incorrect batch size (expected 2, but found {}.".format(
                    len(record_batch)
                )
            )

            batch_received.set()

        consumer = LogRecordConsumer(record_queue, handler, batch_size=2)
        consumer.start()

        record_queue.put("Item1")
        record_queue.put("Item2")

        batch_received.wait(timeout=2000)

        consumer.stop()

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

        expect.log_message(record, "'Foo', Arg2 = 'Bar', Arg3 = 7")

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
