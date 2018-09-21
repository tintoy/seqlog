#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_seqlog
----------------------------------

Tests for `seqlog` module's `configure_from_file`.
"""

import json.encoder
from seqlog.structured_logging import _ensure_class


class TestResolveClass(object):
    def test_ensure_class_default_json_encoder_str(self):
        """
        Verify that the default json.encoder.JSONEncoder class can be resolved from a string.
        """

        resolved_class = _ensure_class('json.encoder.JSONEncoder', compatible_class=json.encoder.JSONEncoder)
        assert resolved_class == json.encoder.JSONEncoder

    def test_ensure_class_default_json_encoder_class(self):
        """
        Verify that the default json.encoder.JSONEncoder class can be resolved from itself.
        """

        resolved_class = _ensure_class(json.encoder.JSONEncoder, compatible_class=json.encoder.JSONEncoder)
        assert resolved_class == json.encoder.JSONEncoder

    def test_ensure_class_test_json_encoder_str(self):
        """
        Verify that the default tests.test_resolve_class.TestJSONEncoder class can be resolved from a string.
        """

        resolved_class = _ensure_class('tests.test_resolve_class.TestJSONEncoder', compatible_class=json.encoder.JSONEncoder)
        assert resolved_class == TestJSONEncoder

    def test_ensure_class_test_json_encoder_class(self):
        """
        Verify that the default tests.test_resolve_class.TestJSONEncoder class can be resolved from itself.
        """

        resolved_class = _ensure_class(TestJSONEncoder, compatible_class=json.encoder.JSONEncoder)
        assert resolved_class == TestJSONEncoder

    def test_ensure_class_not_an_encoder_str(self):
        """
        Verify that the default tests.test_resolve_class.TestNotAnEncoder class cannot be resolved from a string.
        """

        try:
            _ensure_class('tests.test_resolve_class.TestNotAnEncoder', compatible_class=json.encoder.JSONEncoder)
        except ValueError:
            pass
        else:
            raise AssertionError('_ensure_class should not permit a non-JSONEncoder class to be resolved if compatible_class is specified')

    def test_ensure_class_not_an_encoder_class(self):
        """
        Verify that the default tests.test_resolve_class.TestNotAnEncoder class can be resolved from itself.
        """

        try:
            _ensure_class(TestNotAnEncoder, compatible_class=json.encoder.JSONEncoder)
        except ValueError:
            pass
        else:
            raise AssertionError('_ensure_class should not permit a non-JSONEncoder class to be resolved if compatible_class is specified')


class TestJSONEncoder(json.encoder.JSONEncoder):
    def __init__(self):
        super().__init__(self)


class TestNotAnEncoder(object):
    def __init__(self):
        super().__init__(self)
