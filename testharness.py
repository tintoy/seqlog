#!/usr/bin/env python3

import logging
import socket
import os
from time import sleep

import seqlog

server_url = os.getenv("SEQ_SERVER_URL", "http://localhost:5341/")
api_key = os.getenv("SEQ_API_KEY", "")

print("Logging to Seq server '{}' (API key = '{}').".format(server_url, api_key))

log_handler = seqlog.log_to_seq(
    server_url,
    api_key,
    level=logging.INFO,
    auto_flush_timeout=0.2,
    additional_handlers=[logging.StreamHandler()],
    override_root_logger=True
)

print("Running...")

logging.info("Hi, {name}. {greeting}", name="Root logger", greeting="Nice to meet you")

logger1 = logging.getLogger("A")
logger1.info("Hi, {name}! {greeting}", name="world", greeting="Nice to meet you")

logger2 = logging.getLogger("A.B")
logger2.info("Bye, {name}! {greeting}", name="moon", greeting="Nice to meet you")

logger3 = logging.getLogger("C")
logger3.info("By, %s!", "moon")

print("Sleeping...")
sleep(0.5)
print("Done.")
