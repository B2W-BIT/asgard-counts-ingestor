import unittest
from unittest import mock
import os
import sys

from countsingestor import conf

class RoutesTest(unittest.TestCase):

    def tearDown(self):
        # Hack porque um mesmo módulo so é importado uma vez
        sys.modules.pop('countsingestor.routes', None)

    def test_instantiate_app_with_correct_params(self):
        with mock.patch.multiple(conf,
                                 RABBITMQ_HOST="10.0.0.4",
                                 RABBITMQ_USER="user",
                                 RABBITMQ_PWD="secret",
                                 RABBITMQ_PREFETCH=1024):
            from countsingestor.routes import app
            self.assertEqual("10.0.0.4", app.host)
            self.assertEqual("user", app.user)
            self.assertEqual("secret", app.password)
            self.assertEqual(1024, app.prefetch_count)

    def test_use_correct_vhost(self):
        expected_vhost_name = "my-vhost"
        with mock.patch.multiple(conf,
                                 RABBITMQ_VHOST=expected_vhost_name):
            from countsingestor.routes import app, counts_ingestor
            self.assertEqual(1, len(app.routes_registry.keys()))
            self.assertEqual(expected_vhost_name, app.routes_registry[counts_ingestor]['options']['vhost'])

    def test_use_correct_queue_names(self):
        expected_queue_names = ["asagrd/counts", "asgard/counts/errors", "asgard/other"]
        with mock.patch.multiple(conf,
                                 COUNTS_QUEUE_NAMES=expected_queue_names):
            from countsingestor.routes import app, counts_ingestor
            self.assertEqual(1, len(app.routes_registry.keys()))
            self.assertEqual(expected_queue_names, app.routes_registry[counts_ingestor]['route'])
