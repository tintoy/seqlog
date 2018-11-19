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
        Verify that the default tests.test_resolve_class.JSONEncoderTest class can be resolved from a string.
        """

        resolved_class = _ensure_class('tests.test_resolve_class.JSONEncoderTest', compatible_class=json.encoder.JSONEncoder)
        assert resolved_class == JSONEncoderTest

    def test_ensure_class_test_json_encoder_class(self):
        """
        Verify that the default tests.test_resolve_class.JSONEncoderTest class can be resolved from itself.
        """

        resolved_class = _ensure_class(JSONEncoderTest, compatible_class=json.encoder.JSONEncoder)
        assert resolved_class == JSONEncoderTest

    def test_ensure_class_not_an_encoder_str(self):
        """
        Verify that the default tests.test_resolve_class.NotAnEncoderTest class cannot be resolved from a string.
        """

        try:
            _ensure_class('tests.test_resolve_class.NotAnEncoderTest', compatible_class=json.encoder.JSONEncoder)
        except ValueError:
            pass
        else:
            raise AssertionError('_ensure_class should not permit a non-JSONEncoder class to be resolved if compatible_class is specified')

    def test_ensure_class_not_an_encoder_class(self):
        """
        Verify that the default tests.test_resolve_class.NotAnEncoderTest class can be resolved from itself.
        """

        try:
            _ensure_class(NotAnEncoderTest, compatible_class=json.encoder.JSONEncoder)
        except ValueError:
            pass
        else:
            raise AssertionError('_ensure_class should not permit a non-JSONEncoder class to be resolved if compatible_class is specified')


class JSONEncoderTest(json.encoder.JSONEncoder):
    def __init__(self):
        super().__init__(self)


class NotAnEncoderTest(object):
    def __init__(self):
        super().__init__(self)
