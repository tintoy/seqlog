=======
History
=======

0.0.1 (2016-07-07)
------------------

* First release on PyPI.

0.0.7 (2016-07-09)
------------------

* ``log_to_seq`` now returns the SeqLogHandler to enable forced flushing of log records to Seq.
* Change ``auto_flush_timeout`` to a ``float`` representing seconds (instead of milliseconds).
* Update ``testharness.py`` to actually log to Seq.
  You can override the server URL and API key using the ``SEQ_SERVER_URL`` and ``SEQ_API_KEY`` environment variables.
* Update usage information in documentation.
* Python 3 only for now (sorry, but logging in Python 2 doesn't have all the required extensibility points). If the need to support Python 2 becomes great enough then I'll try to find a way.

0.1.0 (2016-07-09)
------------------

* Proper versioning starts today :)

0.2.0 (2016-07-09)
------------------

* Support for configuring additional log handlers when calling log_to_seq.
* Support for global log properties (statically-configured properties that are added to all outgoing log entries).

0.3.0 (2016-11-16)
------------------

* Fix for intermittent "RuntimeError: The content for this response was already consumed" when publishing log entries (#1)
