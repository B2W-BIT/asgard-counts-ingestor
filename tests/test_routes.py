import unittest
from unittest import mock
import os
import sys
import importlib

from countsingestor import conf
from countsingestor import routes

class RoutesTest(unittest.TestCase):

    def test_instantiate_app_with_correct_params(self):
        with mock.patch.multiple(conf,
                                 RABBITMQ_HOST="10.0.0.4",
                                 RABBITMQ_USER="user",
                                 RABBITMQ_PWD="secret",
                                 RABBITMQ_PREFETCH=1024):
            importlib.reload(routes)
            self.assertEqual("10.0.0.4", routes.app.host)
            self.assertEqual("user", routes.app.user)
            self.assertEqual("secret", routes.app.password)
            self.assertEqual(1024, routes.app.prefetch_count)

    def test_use_correct_vhost(self):
        expected_vhost_name = "my-vhost"
        with mock.patch.multiple(conf,
                                 RABBITMQ_VHOST=expected_vhost_name):
            importlib.reload(routes)
            self.assertEqual(1, len(routes.app.routes_registry.keys()))
            self.assertEqual(expected_vhost_name, routes.app.routes_registry[routes.counts_ingestor]['options']['vhost'])

    def test_use_correct_queue_names(self):
        expected_queue_names = ["asagrd/counts", "asgard/counts/errors", "asgard/other"]
        with mock.patch.multiple(conf,
                                 COUNTS_QUEUE_NAMES=expected_queue_names):
            importlib.reload(routes)
            self.assertEqual(1, len(routes.app.routes_registry.keys()))
            self.assertEqual(expected_queue_names, routes.app.routes_registry[routes.counts_ingestor]['route'])
