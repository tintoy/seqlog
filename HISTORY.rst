=======
History
=======

0.4.1 (2025-05-11)
------------------

* A bugfix to catch `ValueError`\s when formatting messages (tintoy/seqlog#87).

0.4.0 (2024-12-08)
------------------

* You can enable and disable all of the feature flags at runtime
* Added support for the `CLEF submission format <https://docs.datalust.co/docs/posting-raw-events>`_.
* Fixed a bug wherein configure_from_file would not propagate feature flags
* You can pass bare strings in the exc_info field (although this serves the same purpose as enabling STACK_INFO and using that variable)
* A bugfix wherein `configure_from_file` would not relay it's arguments to `configure_from_dict` in the correct order

0.3.31 (2024-04-27)
-------------------

* Fix incorrect stack-trace in logged exceptions (tintoy/seqlog#69).

0.3.30 (2023-10-28)
-------------------

* Hide errors caused by unavailable Seq server (tintoy/seqlog#61).

0.3.29 (2023-08-24)
-------------------

* Fix type-hint on `set_global_log_properties` (tintoy/seqlog#60).

0.3.28 (2023-08-13)
-------------------

* Improve behaviour of `best_effort_json_encode` so it does not convert JSON to a string (tintoy/seqlog#59).

0.3.27 (2023-08-03)
-------------------

* StructuredLogRecord now converts non-string msg to string (tintoy/seqlog#51).
* Improve logging-error logging behaviour when a failure handler has been registered (tintoy/seqlog#52).
* Improve implementation of `SeqLogHandler._build_event_data()` (tintoy/seqlog#42).

0.3.26 (2023-04-20)
-------------------

* Don't attempt to JSON-encode log event properties that are already strings (tintoy/seqlog#42, tintoy/seqlog#48).

0.3.25 (2023-04-18)
-------------------

* Temporarily revert changes for including `stack_info` (if present) in event payloads sent to Seq (tintoy/seqlog#42).

0.3.24 (2023-04-14)
-------------------

* Include `stack_info` (if present) in event payloads sent to Seq (tintoy/seqlog#42).

0.3.22 (TBA)
------------

* Add support for handling extra log properties via the `extra` argument (tintoy/seqlog#41).

0.3.21 (TBA)
------------

* added checking if None was passed as element of a message
* fixed #13

0.3.20 (2020-10-15)
-------------------

* Added a callable to be called each time log submission fails

0.3.19 (2020-10-15)
-------------------

* Fixed logging messages containing braces

0.3.18 (2020-09-13)
-------------------

* Add an option to specify a callable in global properties

0.3.17 (2020-02-14)
-------------------

* Improve handling of log entries with log-record arguments of type "bytes" (tintoy/seqlog#25).

0.3.16 (2019-11-02)
-------------------

* Pass exception details when posting events to Seq (tintoy/seqlog#22).

0.3.15 (2018-11-20)
-------------------

* Fix deprecated use of `yaml.load` (tintoy/seqlog#20).

0.3.13 (2018-11-20)
-------------------

* Explicitly set ``Content-Type`` header to ``application/json`` when posting events to Seq (tintoy/seqlog#17).

0.3.12 (2018-11-19)
-------------------

* If logging fails to submit an event to Seq then log the response body, if available (tintoy/seqlog#17).

0.3.11 (2018-09-22)
-------------------

* Support custom ``JSONEncoder`` implementations (tintoy/seqlog#7 and tintoy/seqlog#13).

0.3.10 (2018-08-11)
-------------------

* Fix incorrect behaviour when configuring logging from a file (tintoy/seqlog#10).  
  **Breaking change**: Configuring logging from file or dict will now by default override the default logger class to be ``StructuredLogger`` (this can be reverted to previous behaviour by passing ``use_structured_logger=False``).

0.3.9 (2018-01-09)
------------------

* Add PyYAML as a dependency (tintoy/seqlog#6).

0.3.8 (2018-01-05)
------------------

* Improve documentation for logging configuration from file (#3)

0.3.7 (2018-01-05)
------------------

* Implement and document logging configuration from file (#3)

0.3.4 (2017-11-27)
------------------

* Fix sample code (#2).

0.3.3 (2016-11-18)
------------------

* Use streaming mode when posting to Seq (#1)

0.3.2 (2016-11-18)
------------------

* Updated release notes

0.3.1 (2016-11-18)
------------------

* Further work relating to intermittent "RuntimeError: The content for this response was already consumed" when publishing log entries (#1)

0.3.0 (2016-11-16)
------------------

* Fix for intermittent "RuntimeError: The content for this response was already consumed" when publishing log entries (#1)

0.2.0 (2016-07-09)
------------------

* Support for configuring additional log handlers when calling log_to_seq.
* Support for global log properties (statically-configured properties that are added to all outgoing log entries).

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

