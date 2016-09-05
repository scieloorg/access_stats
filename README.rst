Access Stats
============

Web API and RPC Server to retrieve statistics from the documents and journals published at
the SciELO Network databases.

Build Status
============

.. image:: https://travis-ci.org/scieloorg/access_stats.svg
    :target: https://travis-ci.org/scieloorg/access_stats


Docker
======

Status
------

.. image:: https://images.microbadger.com/badges/image/scieloorg/access_stats.svg
    :target: https://hub.docker.com/r/scieloorg/access_stats
    
.. image:: https://images.microbadger.com/badges/version/scieloorg/access_stats.svg
    :target: https://hub.docker.com/r/scieloorg/access_stats


Como utilizar esta imagem
-------------------------

$ docker run --name my-access_stats -d my-access_stats

Como configurar o ELASTICSEARCH_HOST

$ docker run --name my-access_stats -e ELASTICSEARCH=my_eshost:9200 -d my-access_stats

Os serviços ativos nesta imagem são:

Web API: 127.0.0.1:8000
Thrift Server: 127.0.0.1:11620

É possível mapear essas portas para o hosting dos containers da seguinte forma:

$ docker run --name my-access_stats -e ELASTICSEARCH=my_eshost:9200 -p 8000:8000 -p 11620:11620 -d my-access_stats
