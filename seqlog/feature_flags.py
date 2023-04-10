# -*- coding: utf-8 -*-

from enum import Enum


class FeatureFlag(Enum):
    """
    Well-known feature flags.
    """

    def __new__(cls, value, doc=None):
        self = object.__new__(cls)  # calling super().__new__(value) here would fail
        self._value_ = value

        if doc is not None:
            self.__doc__ = doc

        return self

    EXTRA_PROPERTIES = 1,
    "Support passing of additional properties to log via the `extra` argument?"

    STACK_INFO = 2,
    "Support attaching of stack-trace information (if available) to log records?"


_features = {
    FeatureFlag.EXTRA_PROPERTIES: False,
    FeatureFlag.STACK_INFO: False,
}
"Configured feature flags"


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


def configure_feature(feature: FeatureFlag, enable: bool):
    """
    Enable or disable a feature.

    :param feature: A `FeatureFlag` value representing the feature to configure.
    :type feature: FeatureFlag
    :param enable: `True`, to enable the feature; `False` to disable it.
    :type enable: bool
    """

    _features[feature] = enable
