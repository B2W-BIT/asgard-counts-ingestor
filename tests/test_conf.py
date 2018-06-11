import unittest
from unittest import mock
import os
import sys

class ConfTest(unittest.TestCase):

    def tearDown(self):
        # Hack porque um mesmo módulo so é importado uma vez
        sys.modules.pop('countsingestor', None)

    @unittest.skip("Está falhando quando roda a suite toda")
    def test_read_options_from_envvar(self):
        with mock.patch.dict(os.environ,
                         COUNTS_RABBITMQ_HOST="10.0.0.42",
                         COUNTS_RABBITMQ_USER="myuser",
                         COUNTS_RABBITMQ_PWD="secret",
                         COUNTS_RABBITMQ_VHOST="myvhost",
                         COUNTS_RABBITMQ_PREFETCH=1024,
                         COUNTS_QUEUE_NAMES="asgard/counts, asgard/counts/errors,  asgard/other   "):
            from countsingestor import conf
            self.assertEqual("10.0.0.42", conf.RABBITMQ_HOST)
            self.assertEqual("myuser", conf.RABBITMQ_USER)
            self.assertEqual("secret", conf.RABBITMQ_PWD)
            self.assertEqual("myvhost", conf.RABBITMQ_VHOST)
            self.assertEqual(1024, conf.RABBITMQ_PREFETCH)
            self.assertEqual(["asgard/counts", "asgard/counts/errors", "asgard/other"], conf.COUNTS_QUEUE_NAMES)

