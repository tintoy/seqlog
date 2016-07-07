#!/usr/bin/env python3

import logging

import seqlog

seqlog.log_to_console(level=logging.INFO, override_root_logger=True)

logger1 = logging.getLogger("A")
logger1.info("Hello, {name}!", name="world")

logger2 = logging.getLogger("A.B")
logger2.info("Goodbye, {name}!", name="moon")

logging.info("Hello, {name}.", name="Root logger")

logger3 = logging.getLogger("C")
logger3.info("Goodbye, %s!", "moon")
