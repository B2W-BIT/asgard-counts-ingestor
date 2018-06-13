
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
