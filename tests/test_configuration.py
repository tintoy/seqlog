#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_seqlog
----------------------------------

Tests for `seqlog.config_from_*` module.
"""
import os

import yaml

from seqlog import configure_from_file, configure_from_dict

CFG_CONTENT = """# This is the Python logging schema version (currently, only the value 1 is supported here).
version: 1

# Configure logging from scratch.
disable_existing_loggers: True

# Configure the root logger to use Seq
root:
  level: 'DEBUG'
  handlers:
    - console
    - seq
handlers:
  console:
    class: seqlog.structured_logging.ConsoleStructuredLogHandler
    formatter: standard
  seq:
    class: seqlog.structured_logging.SeqLogHandler
    formatter: standard
    server_url: 'http://localhost'
formatters:
  standard:
    format: '[%(levelname)s] %(asctime)s %(name)s: %(message)s'
"""

class TestConfiguration(object):
    def test_valid_config(self):
        try:
            with open('test', 'w', encoding='utf-8') as w_out:
                w_out.write(CFG_CONTENT)
            configure_from_file('test')

            with open('test', 'r', encoding='utf-8') as r_in:
                dct = yaml.load(r_in, Loader=yaml.Loader)
                configure_from_dict(dct)
        finally:
            os.unlink('test')
