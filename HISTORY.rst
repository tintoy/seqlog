=======
History
=======

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

