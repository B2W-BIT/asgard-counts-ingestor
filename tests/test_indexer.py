import unittest
from unittest import mock
import asynctest
from asynctest import CoroutineMock

from countsingestor.indexer import CountsIndexer

class IndexerTest(asynctest.TestCase):
    """
    Exemplo de mensagem de logs que foram parseados corretamente:
    {
       "key" : "counts.ok.1m",
       "payload" : {
          "count_rate" : 0.01,
          "bytes" : 66,
          "count" : 1,
          "bytes_rate" : 1.09,
          "tag" : "asgard.app.infra.asgard.scoutapp.fluentd"
       },
       "timestamp" : 1528506314
    }

    Exemplo de mensagem de logs que provocaram erro de parsing.

    {
       "key" : "counts.errors.1m",
       "timestamp" : 1528527244,
       "payload" : {
          "tag" : "errors.asgard.app.infra.asgard.scoutapp.fluentd",
          "bytes" : 89175,
          "bytes_rate" : 1474.02,
          "count_rate" : 5.6,
          "count" : 339
       }
    }
    """


    async def setUp(self):
        super().setUp()
        self.counts_ok_fixture = {
           "key" : "counts.ok.1m",
           "payload" : {
              "count_rate" : 0.01,
              "bytes" : 66,
              "count" : 1,
              "bytes_rate" : 1.09,
              "tag" : "asgard.app.infra.asgard.scoutapp.fluentd"
           },
           "timestamp" : 1528506314
        }
        self.counts_error_fixture = {
           "key" : "counts.errors.1m",
           "timestamp" : 1528527244,
           "payload" : {
              "tag" : "errors.asgard.app.infra.asgard.scoutapp.fluentd",
              "bytes" : 89175,
              "bytes_rate" : 1474.02,
              "count_rate" : 5.6,
              "count" : 339
           }
        }

        self.indexer = CountsIndexer(elasticsearch=CoroutineMock(index=CoroutineMock()))

    def test_detect_log_type(self):
        """
        Detectamos qual o tipo de contagem de log: OK ou ERROR
        """
        self.assertEqual("OK", self.indexer._log_type("asgard.app.infra.asgard.scoutapp.fluentd"))
        self.assertEqual("ERROR", self.indexer._log_type("errors.asgard.app.infra.asgard.scoutapp.fluentd"))

    def test_extract_app_name(self):
        self.assertEqual("/infra/asgard/scoutapp/fluentd", self.indexer._extract_app_name("asgard.app.infra.asgard.scoutapp.fluentd"))
        self.assertEqual("/infra/asgard/scoutapp/fluentd", self.indexer._extract_app_name("errors.asgard.app.infra.asgard.scoutapp.fluentd"))
        self.assertEqual("/infra/asgard/errors/scoutapp/fluentd", self.indexer._extract_app_name("errors.asgard.app.infra.asgard.errors.scoutapp.fluentd"))

    async def test_adiciona_marcacao_que_indica_se_o_doc_pertence_a_um_erro_de_parsing(self):
        """
        Vamos adicionar um campo indicando de onte a mensagem veio: OK ou ERROR
        Isso vai ajudar quando juntarmos os dois indices e quisermos saber/contar
        estatísticas de logs OK e de logs que provocaram erro de parsing.

        """
        await self.indexer.index(self.counts_ok_fixture)
        await self.indexer.index(self.counts_error_fixture)

        self.indexer.elasticsearch.index.assert_awaited()

        call_keywork_arguments = self.indexer.elasticsearch.index.await_args_list[0][1]
        self.assertEqual("OK", call_keywork_arguments['body']['log_parse'])

        # segunda chamada de indexação, para a firute de counts_error
        call_error_keywork_arguments = self.indexer.elasticsearch.index.await_args_list[1][1]
        self.assertEqual("ERROR", call_error_keywork_arguments['body']['log_parse'])

    async def test_choose_the_right_index_name_based_on_count_type(self):
        """
        Vamos gravar as contagem de logs válidos e inválidos em índices
        diferentes.
        """

        await self.indexer.index(self.counts_ok_fixture)
        await self.indexer.index(self.counts_error_fixture)

        self.indexer.elasticsearch.index.assert_awaited()
        self.assertEqual([
                mock.call(index="asgard-counts-ok", doc_type="counts", body=mock.ANY),
                mock.call(index="asgard-counts-errors", doc_type="counts", body=mock.ANY),
                ], self.indexer.elasticsearch.index.await_args_list)



    async def test_extract_app_name_and_add_it_to_document(self):
        """
        O documento final tem o ID da app, exatamente igual ao ID que está
        no asgard, apenas com o namespace adicionado.
        Devemos também remover o campo original, `tag`.
        """
        await self.indexer.index(self.counts_ok_fixture)
        await self.indexer.index(self.counts_error_fixture)

        self.indexer.elasticsearch.index.assert_awaited()


        call_keywork_arguments = self.indexer.elasticsearch.index.await_args_list[0][1]
        self.assertEqual("/infra/asgard/scoutapp/fluentd", call_keywork_arguments['body']['appname'])
        self.assertTrue('tag' not in call_keywork_arguments['body'])

        # segunda chamada de indexação, para a firute de counts_error
        call_error_keywork_arguments = self.indexer.elasticsearch.index.await_args_list[1][1]
        self.assertEqual("/infra/asgard/scoutapp/fluentd", call_error_keywork_arguments['body']['appname'])
        self.assertTrue('tag' not in call_error_keywork_arguments['body'])


    async def test_convert_timestamp_to_string(self):
        """
        Usaremos o mesmo campo, vamos apenas substituir o valor que está lá.
        """
        await self.indexer.index(self.counts_ok_fixture)

        self.indexer.elasticsearch.index.assert_awaited()
        call_keywork_arguments = self.indexer.elasticsearch.index.await_args_list[0][1]
        self.assertEqual("2018-06-09T01:05:14", call_keywork_arguments['body']['timestamp'])

    async def test_trasnform_field_names(self):
        """
        Vamos trocar alguns nomes de campos, como por exemplo:
            * bytes_rate -> bytes/s
        """
        await self.indexer.index(self.counts_ok_fixture)

        self.indexer.elasticsearch.index.assert_awaited()
        call_keywork_arguments = self.indexer.elasticsearch.index.await_args_list[0][1]
        self.assertEqual(0.01, call_keywork_arguments['body']['count/s'])
        self.assertEqual(1.09, call_keywork_arguments['body']['bytes/s'])

    async def test_move_todos_os_campos_para_a_raiz_do_documento(self):
        self.maxDiff = None
        """
        Os campos estão sempre dentro da key `payload`. Vamos mover todo mundo paraa raiz do
        documento
        Devemos conferir também que o campo payload não existe mais
        """
        expected_body = {
            "log_parse": "ERROR",
            "count/s" : 5.6,
            "bytes" : 89175,
            "count" : 339,
            "bytes/s" : 1474.02,
            "appname" : "/infra/asgard/scoutapp/fluentd",
            "timestamp": "2018-06-09T06:54:04",
        }
        await self.indexer.index(self.counts_error_fixture)

        self.indexer.elasticsearch.index.assert_awaited()
        call_keywork_arguments = self.indexer.elasticsearch.index.await_args_list[0][1]
        print(call_keywork_arguments['body'])
        self.assertDictEqual(expected_body, call_keywork_arguments['body'])

