#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_seqlog
----------------------------------

Tests for `seqlog.config_from_*` module.
"""
import logging.config
import os

import yaml

from tests.test_structured_logger import create_logger

CFG_CONTENT = """
# This is the Python logging schema version (currently, only the value 1 is supported here).
---
version: 1

# Configure logging from scratch.
disable_existing_loggers: True

# Configure the root logger to use Seq
root:
  level: 'DEBUG'
  handlers:
    - console
handlers:
  console:
    class: seqlog.structured_logging.ConsoleStructuredLogHandler
    formatter: standard
    override_root_logger: True
    use_structured_logging: True
formatters:
  standard:
    format: '[%(levelname)s] %(asctime)s %(name)s: %(message)s'
"""


class TestConfiguration(object):
    def test_valid_config(self):

        try:
            with open('test.yaml', 'w', encoding='utf-8') as w_out:
                w_out.write(CFG_CONTENT)

            with open('test.yaml', 'r', encoding='utf-8') as r_in:
                dct = yaml.load(r_in, Loader=yaml.Loader)
                logging.config.dictConfig(dct)
        finally:
            os.unlink('test.yaml')
        logger, handler = create_logger()
        logger.warning('This is a {message}', message='message')
        assert handler.records[0].getMessage() == 'This is a message'
