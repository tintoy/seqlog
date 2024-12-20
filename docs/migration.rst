===============================
Migration guide from 0.4 to 0.5
===============================

First of all, the official way to configure Seq is via

.. autofunction:: seqlog.configure_from_dict

Alternatively you can call

.. autofunction:: seqlog.configure_from_file


.. warning:: DO NOT call :code:`logging.config.fromDict`

Then, FeatureFlags were completely obliterated and moved to SeqLogHandler's constructor.

Then, the SeqLogHandler accepts way more arguments that you can define in this dict:

.. autoclass:: seqlog.structured_logging.SeqLogHandler
    :members:

