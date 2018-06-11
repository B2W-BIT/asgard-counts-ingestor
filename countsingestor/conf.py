import os
import logging

from simple_json_logger import JsonLogger
from aioelasticsearch import Elasticsearch

from asgard.sdk.options import get_option

LOGLEVEL = os.getenv("ASGARD_LOGLEVEL", "INFO")

logger = JsonLogger(flatten=True)
logger.setLevel(getattr(logging, LOGLEVEL, logging.INFO))

ELASTIC_SEARCH_ADDRESSES = get_option("ELASTICSEARCH", "ADDRESS")

elasticsearch = Elasticsearch(hosts=ELASTIC_SEARCH_ADDRESSES)

RABBITMQ_HOST = os.getenv("COUNTS_RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_USER = os.getenv("COUNTS_RABBITMQ_USER", "guest")
RABBITMQ_PWD = os.getenv("COUNTS_RABBITMQ_PWD", "guest")
RABBITMQ_PREFETCH = os.getenv("COUNTS_RABBITMQ_PREFETCH", 32)
RABBITMQ_VHOST = os.getenv("COUNTS_RABBITMQ_VHOST", "/")
COUNTS_QUEUE_NAMES = [item.strip() for item in os.getenv("COUNTS_QUEUE_NAMES", "").split(",")]
