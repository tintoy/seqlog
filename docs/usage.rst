=====
Usage
=====

Configure logging programmatically
----------------------------------

.. code-block:: python

   import seqlog

   seqlog.log_to_seq(
      server_url="http://my-seq-server:5341/",
      api_key="My API Key",
      level=logging.INFO,
      batch_size=10,
      auto_flush_timeout=10,  # seconds
      override_root_logger=True,
      json_encoder_class=json.encoder.JSONEncoder,  # Optional; only specify this if you want to use a custom JSON encoder
      support_extra_properties=True # Optional; only specify this if you want to pass additional log record properties via the "extra" argument.
   )

For the best experience, use ``{x}``-style named format arguments (passing those format arguments as keyword arguments to the log functions ``info``, ``warning``, ``error``, ``critical``, etc).
Using unnamed "holes" (i.e. ``{}``) is not currently supported.

For example:

.. code-block:: python

   logging.info("Hello, {name}!", name="World")

If you specify ordinal arguments, the log message is interpreted as a "%s"-style format string.
The ordinal format arguments are stored in the log entry properties using the 0-based ordinal index as the property name.

.. code-block:: python

   logging.info("Hello, %s!", "World")

Note that mixing named and ordinal arguments is not currently supported.

Configure logging from a file
-----------------------------

Seqlog can also use a YAML-format file to describe the desired logging configuration. This file has the schema specified in Python's `logging.config <https://docs.python.org/3/library/logging.config.html#logging-config-dictschema>`_ module.

First, create your configuration file (e.g. ``/foo/bar/my_config.yml``):

.. code-block:: yaml

    # This is the Python logging schema version (currently, only the value 1 is supported here).
    version: 1

    # Configure logging from scratch.
    disable_existing_loggers: True

    # Configure the root logger to use Seq
    root:
      level: INFO
      handlers:
      - seq
      - console

    # You can also configure non-root loggers.
    loggers:
      another_logger:
          propagate: False
          level: INFO
          handlers:
          - seq
          - console

    handlers:
    # Log to STDOUT
      console:
        class: seqlog.structured_logging.ConsoleStructuredLogHandler
        formatter: seq

    # Log to Seq
      seq:
        class: seqlog.structured_logging.SeqLogHandler
        formatter: seq

        # Seq-specific settings (add any others you need, they're just kwargs for SeqLogHandler's constructor).
        server_url: 'http://localhost:5341'
        api_key: 'your_api_key_if_you_have_one'

        # Use a custom JSON encoder, if you need to.
        json_encoder_class: json.encoder.JSONEncoder

    formatters:
      seq:
        style: '{'

Then, call ``seqlog.configure_from_file()``:

.. code-block:: python

    seqlog.configure_from_file('/foo/bar/my_config.yml')

    # Use the root logger.
    root_logger = logging.getLogger()
    root_logger.info('This is the root logger.')

    # Use another logger
    another_logger = logging.getLogger('another_logger')
    another_logger.info('This is another logger.')

Configuring logging from a dictionary
-------------------------------------

Seqlog can also use a dictionary to describe the desired logging configuration.
This dictionary has the schema specified in Python's `logging.config <https://docs.python.org/3/library/logging.config.html#logging-config-dictschema>`_ module.

.. code-block:: python

    config = {
      # configuration goes here
    }

    seqlog.configure_from_dict(config)

    # Use the root logger.
    root_logger = logging.getLogger()
    root_logger.info('This is the root logger.')

    # Use another logger
    another_logger = logging.getLogger('another_logger')
    another_logger.info('This is another logger.')

Batching and auto-flush
-----------------------

By default SeqLog will wait until it has a batch of 10 messages before sending them to Seq.
You can control the batch size by passing a value for ``batch_size``.

If you also want it to publish the current batch of events when not enough of them have arrived within a certain period, you can pass ``auto_flush_timeout`` (a ``float`` representing the number of seconds before an incomplete batch is published).

Overriding the root logger
--------------------------

By default, SeqLog does not modify the root logger (and so calls to ``logging.info()`` and friends do not support named format arguments).
To also override the root logger, pass ``True`` for ``override_root_logger``.

Additional LogHandlers
----------------------

By default, ``log_to_seq`` only configures a single SeqLogHandler.

To configure additional LogHandlers, pass them via ``additional_handlers``.

Global log properties
---------------------

SeqLog can also add static properties to each log entry that is sent to Seq.
By default, the following properties are added:

* ``MachineName`` The local machine's fully-qualified host name.
* ``ProcessId`` The current process Id.

To configure global log properties, call ``set_global_log_properties``, passing the properties as keyword arguments:

.. code-block:: python

    import seqlog

    seqlog.set_global_log_properties(
        GlobalProperty1="foo",
        GlobalProperty2="bar"
        GlobalProperty3=26
    )

Note that you can also clear the global log properties (so no properties are added) by calling ``clear_global_log_properties``, and reset the global log properties to their defaults by calling ``reset_global_log_properties``.

Note that is you specify a callable as part of global log properties, it will be called
with no arguments right before logging:

.. code-block:: python

    import seqlog

    def get_trace_id():
        if tracer.active_span is not None:
            return hex(tracer.active_span.context.trace_id)
        else:
            return None

    seqlog.set_global_log_properties(
        trace_id=get_trace_id,
    )

If the callable returns None, it won't be added.

Callback on log submission failure
----------------------------------

If you wish to set a callable to be invoked each time log submission fails, 
use the following function:

.. code-block:: python

    from seqlog import set_callback_on_failure
    
    def handle_a_failure(e):    # type: (requests.RequestException) -> None
        print('Failure occurred during log submission: %s' % (e, ))
        
   set_callback_on_failure(handle_a_failure)

The callable that you provide will accept a single positional argument, 
which is the requests exception instance that was the reason for the fail.

.. note:: This callable will be called only for I/O errors, errors stemming
          from seqlog not being able to convert your records into JSON won't
          show up here!
