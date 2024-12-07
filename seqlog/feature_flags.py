# -*- coding: utf-8 -*-
import typing as tp
from enum import Enum


class FeatureFlag(Enum):
    """
    Well-known feature flags.
    """

    EXTRA_PROPERTIES = 1  #: Support passing of additional properties to log via the `extra` argument?

    STACK_INFO = 2  #: Support attaching of stack-trace information (if available) to log records?

    IGNORE_SEQ_SUBMISSION_ERRORS = 3   #: Ignore errors encountered while sending log records to Seq?

    USE_CLEF = 4    #: Use more modern API to submit log entries


_features = {
    FeatureFlag.EXTRA_PROPERTIES: False,
    FeatureFlag.STACK_INFO: False,
    FeatureFlag.IGNORE_SEQ_SUBMISSION_ERRORS: False,
    FeatureFlag.USE_CLEF: False
}


def is_feature_enabled(feature: FeatureFlag):
    """
    Is a feature enabled?

    :param feature: A `FeatureFlag` value representing the feature.
    :type feature: FeatureFlag
    :return: `True`, if the feature is enabled; otherwise, `False`.
    :rtype: bool
    """

    return _features.get(feature, False)


def enable_feature(feature: FeatureFlag):
    """
    Enable a feature.

    :param feature: A `FeatureFlag` value representing the feature to enable.
    :type feature: FeatureFlag
    """

    configure_feature(feature, True)


def disable_feature(feature: FeatureFlag):
    """
    Disable a feature.

    :param feature: A `FeatureFlag` value representing the feature to disable.
    :type feature: FeatureFlag
    """

    configure_feature(feature, False)


def configure_feature(feature: FeatureFlag, enable: tp.Optional[bool]):
    """
    Enable or disable a feature.

    :param feature: A `FeatureFlag` value representing the feature to configure. If you pass None, it won't get changed.
    :type feature: FeatureFlag
    :param enable: `True`, to enable the feature; `False` to disable it.
    """
    if enable is None:
        return
    _features[feature] = enable
