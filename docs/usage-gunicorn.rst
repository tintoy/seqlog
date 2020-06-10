================
Usage (Gunicorn)
================

Using seqlog with `Gunicorn <https://gunicorn.org/>` involves some additional configuration because of the way Gunicorn uses ``fork`` to create new worker processes.

A custom ``JSONEncoder`` is also used to handle objects that are not `JSON serializable`.

``api/__init__.py``:

.. code-block:: python

  from flask import Flask
  app = Flask(__name__)

``api/gunicorn.py``:

.. code-block:: python

  import multiprocessing

  from api.logging_provider import (
      configure_server_logging,
      configure_worker_logging,
      get_log_config_dict)

  bind = '0.0.0.0:8000'
  workers = (2 * multiprocessing.cpu_count()) + 1

  # Configure logging
  logconfig_dict = get_log_config_dict()


  def when_ready(server):
      configure_server_logging(logconfig_dict)


  def post_worker_init(worker):
      configure_worker_logging(worker, logconfig_dict)

``api/logging_provider.py``:

.. code-block:: python

  import logging
  import seqlog
  import yaml

  from api import app


  def configure_server_logging(log_config_dict):
      seqlog.configure_from_dict(log_config_dict)


  def configure_worker_logging(worker, log_config_dict):
      seqlog.configure_from_dict(log_config_dict)

      with app.app_context():
          logger = logging.getLogger('gunicorn.error')
          app.logger.handlers = logger.handlers
          app.logger.propagate = False
          app.logger.setLevel(logger.level)

      configure_logger(worker.log.access_log)
      configure_logger(worker.log.error_log)


  def configure_logger(logger):
      for handler in logger.handlers:
          if handler.get_name() == 'seq':
              try:
                  handler.consumer.stop()
              except:
                  pass

              try:
                  handler.consumer.start()
              except:
                  pass


  def get_log_config_dict():
      with open('log_config.yml', 'r') as log_config_file:
          log_config_dict = yaml.safe_load(log_config_file.read())

``api/log_config.yml``:

.. code-block:: python

  version: 1

  disable_existing_loggers: True

  root:
    level: DEBUG
    handlers:
    - console
    - seq

  loggers:
    gunicorn.access:
      qualname: gunicorn.access
      propagate: False
      level: DEBUG
      handlers:
      - console
      - seq
    gunicorn.error:
      qualname: gunicorn.error
      propagate: False
      level: DEBUG
      handlers:
      - console
      - seq

  handlers:
    console:
      class: seqlog.structured_logging.ConsoleStructuredLogHandler
      formatter: standard

    seq:
      class: seqlog.structured_logging.SeqLogHandler
      formatter: seq
      server_url: 'http://localhost:5341'
      api_key: ''
      batch_size: 1
      auto_flush_timeout: 5
      json_encoder_class: api.utilities.json_extensions.LoggingJSONEncoder

  formatters: 
    seq:
      style: '{'

    standard:
      format: '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'

``api/utilities/json_extensions.py``

.. code-block:: python

  import json

  class LoggingJSONEncoder(json.JSONEncoder):

      def default(self, obj):
          try:
              return json.JSONEncoder.default(self, obj)
          except:
              return str(obj)