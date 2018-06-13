
from countsingestor import conf
from countsingestor.indexer import CountsIndexer

from asyncworker import App

app = App(host=conf.RABBITMQ_HOST, user=conf.RABBITMQ_USER, password=conf.RABBITMQ_PWD, prefetch_count=conf.RABBITMQ_PREFETCH)

@app.route(conf.COUNTS_QUEUE_NAMES, vhost=conf.RABBITMQ_VHOST)
async def counts_ingestor(message):
    indexer = CountsIndexer(elasticsearch=conf.elasticsearch)
    await indexer.index(message)
