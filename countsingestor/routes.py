
from countsingestor import conf
from countsingestor.indexer import CountsIndexer

from asyncworker import App

app = App(host="127.0.0.1", user="guest", password="guest", prefetch_count=32)


@app.route(["asgard/counts", "asgard/counts/errors"], vhost="fluentd")
async def counts_ingestor(message):
    indexer = CountsIndexer(elasticsearch=conf.elasticsearch)
    await indexer.index(message)
