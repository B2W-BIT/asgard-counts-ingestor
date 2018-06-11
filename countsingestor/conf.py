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
