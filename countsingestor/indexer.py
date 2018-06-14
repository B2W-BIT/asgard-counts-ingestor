from datetime import datetime

from countsingestor import conf

class CountsIndexer:

    ASGARD_TAG_PREFIX = "asgard.app"
    ASGARD_TAG_ERROR_PREFIX = "errors."

    INDEX_NAMES = {
        "counts.ok.1m": "asgard-counts-ok",
        "counts.errors.1m": "asgard-counts-errors"
    }

    def __init__(self, elasticsearch):
        self.elasticsearch = elasticsearch


    async def index(self, document):
        fluentd_tag = document['payload']['tag']
        index_name = self.INDEX_NAMES[document['key']]

        indexed_document = {}

        appname = self._extract_app_name(fluentd_tag)
        count_type = self._log_type(fluentd_tag)
        indexed_document['appname'] = appname
        indexed_document['log_parse'] = count_type

        indexed_document['timestamp'] = datetime.utcfromtimestamp(document['timestamp']).isoformat()
        indexed_document['bytes/s'] = document['payload']['bytes_rate']
        indexed_document['count/s'] = document['payload']['count_rate']
        indexed_document['bytes'] = document['payload']['bytes']
        indexed_document['count'] = document['payload']['count']

        await self.elasticsearch.index(index=index_name, doc_type="counts", body=indexed_document)
        await conf.logger.info({"index-time": 0, "appname": appname, "count-type": count_type})

    def _extract_app_name(self, fluentd_tag):
        remove_errors_prefix = fluentd_tag.replace(self.ASGARD_TAG_ERROR_PREFIX, "", 1)
        parts = remove_errors_prefix.replace(self.ASGARD_TAG_PREFIX, "").split('.')
        return "/".join(parts)

    def _log_type(self, fluentd_tag):
        if fluentd_tag.startswith(self.ASGARD_TAG_ERROR_PREFIX):
            return "ERROR"
        return "OK"
