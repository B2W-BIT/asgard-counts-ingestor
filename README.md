
# Asgard Counts Ingestor

## Propósito

Esse projeto será o responsável por coletar estatísticas de logs das aplicações. Essas estatísticas incluem:

* Contagem de linhas de log por minuto
* Contagem de linhas de logs por segundo
* Contagem de bytes de log por minuto
* Contagem de bytes de logs por segundo

São geradas também as mesmas contagem para tpdas as linhas de logs que não puderam ser parseadas, ou seja,
linhas que o log ingestor não conseguiu parsear.


## Fluxo de coleta

Os logs são enviados para um cluster de fluentd, de lá são parseados e acumulados em um RabbitMQ. Nesse acumulo,
já temos filas específicas só para as contagens de logs. Essas serão as filas que esse projeto vai consumir.

## Exemplo de mensagem contendo uma contagem de log de uma app

Os campos com sufixo `_rate` possuem números que representam taxa por segundo.
Os campos sem sufixo representam a contagem de 1 minuto.

### Logs com Parsing OK

```
{
   "key" : "counts.ok.1m",
   "timestamp" : 1531337806,
   "payload" : {
      "bytes_rate" : 351.97,
      "bytes" : 21294,
      "tag" : "asgard.app.infra.asgard.logs.app-stats-indexer",
      "count_rate" : 1.93,
      "count" : 117
   }
}
```

Essa mensagem possui contagem de logs onde o parsing foi feito com sucesso pelo fluentd. Nesse caso esepcífico a app que gerou esses
dados foi `/asgard/logs/app-stats-indexer` do time cujo namespace é `infra`.

### Logs com erro de parsing

```
{
   "key" : "counts.errors.1m",
   "payload" : {
      "count_rate" : 0.01,
      "tag" : "errors.asgard.app.infra.elk.es",
      "bytes_rate" : 5.98,
      "bytes" : 359,
      "count" : 1
   },
   "timestamp" : 1531337806
}
```

Essa mensagem possui contagem de logs onde o parsing provocou um erro no fluentd, ou seja, os log originais não estavam em formato JSON.
Nesse caso esepcífico a app que gerou esses dados foi `/elk/es` do time cujo namespace é `infra`.

### Exemplos de documento produzido no Elastic Search

```
{
   "_index" : "asgard-counts-ok",
   "_score" : 1,
   "_source" : {
      "timestamp" : "2018-06-11T13:14:17",
      "bytes/s" : 351.97,
      "count/s" : 1.93,
      "bytes" : 21294,
      "appname" : "/asgard/logs/app-stats-indexer",
      "count" : 117,
      "log_parse" : "OK"
   },
   "_type" : "counts",
   "_id" : "AWPvQOK9qGi4lCNUnHp2"
}
```

```
{
   "_score" : 1,
   "_source" : {
      "appname" : "/infra/elk/es",
      "bytes" : 359,
      "count" : 1,
      "bytes/s" : 5.98,
      "count/s" : 0.01,
      "log_parse" : "ERROR",
      "timestamp" : "2018-06-11T12:09:39"
   },
   "_id" : "AWPvQZN4qGi4lCNUnI4R",
   "_index" : "asgard-counts-errors",
   "_type" : "counts"
}
```
