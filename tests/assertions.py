def expect_log_message(record, expected_message):
    """
    Assert that a log record has the expected message.
    :param record: The LogRecord.
    :param expected_message: The expected message.
    """

    actual_message = record.getMessage()

    assert (
        expected_message == actual_message,
        "Unexpected log message: '{}'".format(actual_message)
    )


def expect_log_level(record, expected_level):
    """
    Assert that a log record has the expected level (severity).
    :param record: The LogRecord.
    :param expected_level: The expected level.
    """

    actual_level = record.levelno

    assert (
        expected_level == actual_level,
        "Unexpected log level: '{}'".format(actual_level)
    )


def expect_log_ordinal_args(record, *expected_args):
    """
    Assert that a log record has the expected ordinal format arguments.
    :param record: The LogRecord.
    :param expected_args: The expected level.
    """

    actual_args = record.args
    assert(actual_args is not None, "Log record does not have ordinal format arguments.")

    assert (
        expected_args == actual_args,
        "Unexpected ordinal arguments: {}".format(
            repr(actual_args)
        )
    )


def expect_log_named_args(record, **expected_args):
    """
    Assert that a log record has the expected named format arguments.
    :param record: The LogRecord.
    :param expected_args: The expected named format arguments.
    """

    actual_args = record.log_props
    assert(actual_args is not None, "Log record does not have named format arguments.")

    assert (
        expected_args == actual_args,
        "Unexpected named arguments: {}".format(
            repr(actual_args)
        )
    )
