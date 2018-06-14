import os
import logging
import asyncio

from aiologger.loggers.json import JsonLogger
from aioelasticsearch import Elasticsearch

from asgard.sdk.options import get_option

LOGLEVEL_CONF = os.getenv("ASGARD_COUNTS_LOGLEVEL", "INFO")
loglevel = getattr(logging, LOGLEVEL_CONF, logging.INFO)

logger = None

async def init_logger():
    global logger
    logger = await JsonLogger.with_default_handlers(level=loglevel, flatten=True)

loop = asyncio.get_event_loop()
init_logger_task = loop.create_task(init_logger())

ELASTIC_SEARCH_ADDRESSES = get_option("ELASTICSEARCH", "ADDRESS")

elasticsearch = Elasticsearch(hosts=ELASTIC_SEARCH_ADDRESSES)

RABBITMQ_HOST = os.getenv("COUNTS_RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_USER = os.getenv("COUNTS_RABBITMQ_USER", "guest")
RABBITMQ_PWD = os.getenv("COUNTS_RABBITMQ_PWD", "guest")
RABBITMQ_PREFETCH = int(os.getenv("COUNTS_RABBITMQ_PREFETCH", 32))
RABBITMQ_VHOST = os.getenv("COUNTS_RABBITMQ_VHOST", "/")
COUNTS_QUEUE_NAMES = [item.strip() for item in os.getenv("COUNTS_QUEUE_NAMES", "").split(",")]
