=====
Usage
=====

Configure logging to Seq
------------------------

.. code-block:: python

   import seqlog

   seqlog.log_to_seq(
      server_url="http://my-seq-server:5431/",
      api_key="My API Key"
      level=logging.INFO,
      batch_size=10,
      auto_flush_timeout=10000  # milliseconds
      override_root_logger=True
   )

For the best experience, use "{x}"-style named format arguments (passing those format arguments as keyword arguments to the log functions ``info``, ``warning``, ``error``, ``critical``, etc).
Using unnamed "holes" (i.e. "{}") is not currently supported.

For example:

.. code-block:: python

   logging.info("Hello, {name}!", name="World")

If you specify ordinal arguments, the log message is interpreted as a "%s"-style format string.
The ordinal format arguments are stored in the log entry properties using the 0-based ordinal index as the property name.

.. code-block:: python

   logging.info("Hello, %s!", "World")

Note that mixing named and ordinal arguments is not currently supported.

Batching and auto-flush
-----------------------

By default seqlog will wait until it has a batch of 10 messages before sending them to Seq.
You can control the batch size by passing a value for ``batch_size``.

If you also want it to publish the current batch of events when not enough of them have arrived within a certain period, you can pass ``auto_flush_timeout`` (a ``float`` representing the number of seconds before an incomplete batch is published).

Overriding the root logger
--------------------------

By default, seqlog does not modify the root logger (and so calls to ``logging.info()`` and friends do not support named format arguments)."
To also override the root logger, pass ``True`` for ``override_root_logger``.
