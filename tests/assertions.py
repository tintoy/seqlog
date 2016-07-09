def log_message(record, expected_message):
    """
    Assert that a log record has the expected message.
    :param record: The LogRecord.
    :param expected_message: The expected message.
    """

    actual_message = record.getMessage()

    assert expected_message == actual_message, \
        "Unexpected log message: '{}' (expected '{}')".format(actual_message, expected_message)


def log_template(record, expected_template):
    """
    Assert that a log record has the expected template.
    :param record: The LogRecord.
    :param expected_template: The expected template.
    """

    actual_template = record.msg

    assert expected_template == actual_template, \
        "Unexpected log template: '{}' (expected '{}')".format(actual_template, expected_template)


def log_level(record, expected_level):
    """
    Assert that a log record has the expected level (severity).
    :param record: The LogRecord.
    :param expected_level: The expected level.
    """

    actual_level = record.levelno

    assert expected_level == actual_level, \
        "Unexpected log level: '{}' (expected '{}')".format(actual_level, expected_level)


def log_ordinal_args(record, *expected_args):
    """
    Assert that a log record has the expected ordinal format arguments.
    :param record: The LogRecord.
    :param expected_args: The expected level.
    """

    actual_args = record.args
    assert actual_args, "Log record does not have ordinal format arguments."

    assert expected_args == actual_args, \
        "Unexpected ordinal arguments: {}\nExpected ordinal arguments: {}".format(
            repr(actual_args),
            repr(expected_args)
        )


def log_named_args(record, **expected_args):
    """
    Assert that a log record has the expected named format arguments.
    :param record: The LogRecord.
    :param expected_args: The expected named format arguments.
    """

    actual_args = record.log_props
    assert actual_args, "Log record does not have named format arguments."

    assert expected_args == actual_args, \
        "Unexpected named arguments: {}\nExpected named arguments: {}".format(
            repr(actual_args),
            repr(expected_args)
        )
