"""
Interaction with Rollups Server and other Cartesi-related services
"""
import logging
from os import environ

import requests

logger = logging.getLogger(__name__)

rollup_server = environ.get("ROLLUP_HTTP_SERVER_URL", '')
logger.info(f"HTTP rollup_server url is {rollup_server}")


def send_notice(payload):
    logger.info("Adding notice")
    response = requests.post(rollup_server + "/notice", json=payload)
    logger.info(f"Received notice status {response.status_code} body {response.content}")
    return response.content


def send_report(payload):
    logger.info("Adding report")
    response = requests.post(rollup_server + "/report", json=payload)
    logger.info(f"Received report status {response.status_code}")
    return response.content
