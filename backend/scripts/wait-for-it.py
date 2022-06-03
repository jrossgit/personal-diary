#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import socket
import ssl
import time


LOGGER = logging.getLogger(__name__)
LOGGING_FORMAT = "%(asctime)s %(levelname)-5.5s " \
                 "[%(name)s]:[%(threadName)s] " \
                 "%(message)s"

MAX_DB_CONN_RETRIES = 60
MAX_RABBIT_CONN_RETRIES = 60

TIME_BETWEEN_RETRY = 1
"""Seconds between retry attempt"""


def check_connection(host, port, max_conn_retries, ssl_mode=False):
    """Check socket connection for the host and port

    :param host: String
    :param port: String
    :param max_conn_retries: Integer
    :param ssl_mode: Boolean

    :raises: ConnectionError
    """
    retry_count = 0
    while retry_count < max_conn_retries:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        LOGGER.info(f"Retry number: {retry_count} of {max_conn_retries}")

        if ssl_mode:
            LOGGER.info("Will be checking ssl connection")
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            sock = ssl_context.wrap_socket(sock, server_hostname=host)

        try:
            sock.connect((host, int(port)))
            sock.close()
            return
        except socket.error as ex:
            LOGGER.warning(ex)
            time.sleep(TIME_BETWEEN_RETRY)
            retry_count += 1
        except ValueError as ex:
            LOGGER.warning(ex)
            time.sleep(TIME_BETWEEN_RETRY)
            retry_count += 1

    raise ConnectionError(f"Unable to establish connection "
                          f"with host: {host} and port: {port}")


if __name__ == "__main__":
    exit_code = 1
    logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
    try:

        LOGGER.info("Checking database connection")
        check_connection(
            host=os.environ["SQL_HOST"],
            port=os.environ.get("SQL_PORT", "5432"),
            max_conn_retries=MAX_DB_CONN_RETRIES
        )
        LOGGER.info("Database is ready to be connected")
        exit_code = 0
    except ConnectionError as ex:
        LOGGER.error(ex)

    exit(exit_code)
