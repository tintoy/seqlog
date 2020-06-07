================
Usage (Gunicorn)
================

Using seqlog with `Gunicorn <https://gunicorn.org/>` involves some additional configuration because of the way Gunicorn uses ``fork`` to create new worker processes.

``gunicorn.py``:

.. code-block:: python

  import multiprocessing

  from api.log_config_provider import (
      configure_logging,
      get_log_config_dict,
      set_global_log_properties)

  bind = "0.0.0.0:8000"
  workers = (2 * multiprocessing.cpu_count()) + 1

  # Configure logging
  logconfig_dict = get_log_config_dict()
  set_global_log_properties()

  def post_worker_init(worker):
      configure_logging(logconfig_dict)

``log_config_provider.py``:

.. code-block:: python

  import logging
  import os
  import seqlog
  import socket
  import yaml

  from api import app
  from api.config import AppConfig, LoggingConfig
  from api.constants import APP_CONFIG_FILE, LOG_CONFIG_FILE


  def configure_logging(log_config_dict):
      logging.config.dictConfig(log_config_dict)

      with app.app_context():
          logger = logging.getLogger('gunicorn.error')
          app.logger.handlers = logger.handlers
          app.logger.propagate = False
          app.logger.setLevel(logger.level)

      set_global_log_properties()


  def get_log_config_dict():
      with open(LOG_CONFIG_FILE, 'r') as log_config_file:
          log_config = yaml.safe_load(log_config_file.read())

      logging_config = LoggingConfig(APP_CONFIG_FILE)
      transform_log_config(log_config, logging_config)
      return log_config


  def set_global_log_properties():
      app_config = AppConfig(APP_CONFIG_FILE)
      seqlog.set_global_log_properties(
          ApplicationName=app_config.application_name,
          Environment=app_config.environment,
          MachineName=socket.gethostname(),
          ProcessId=os.getpid())


  def transform_log_config(log_config, logging_config):
      log_config['root']['level'] = logging_config.level
      log_config['loggers']['gunicorn.access']['level'] = logging_config.level
      log_config['loggers']['gunicorn.error']['level'] = logging_config.level
      log_config['handlers']['seq']['server_url'] = logging_config.server_url
      log_config['handlers']['seq']['api_key'] = logging_config.api_key

``log_config.yml``:

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

  formatters: 
    seq:
      style: '{'

    standard:
      format: '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'
