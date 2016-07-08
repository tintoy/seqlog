.. seqlog documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Seq logging adapter for Python
==============================

``seqlog`` is a plugin for Python logging that sends log messages to Seq.

To configure logging to Seq:

.. highlight:: python
    import seqlog

    seqlog.log_to_seq(
        server_url="http://my-seq-server:5431/",
        api_key="My API Key"
        level=logging.INFO,
        batch_size=10,
        auto_flush_timeout=10000  # milliseconds
        override_root_logger=True
    )

For the best experience, use named format arguments (passing those format arguments as keyword arguments to the log functions ``info``, ``warning``, ``error``, ``critical``, etc).

For example:

.. highlight:: python
    logging.info("Hello, {name}!", name="World")

Contents:

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   Modules <api/modules>
   contributing
   authors
   history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
