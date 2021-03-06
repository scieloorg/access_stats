# coding: utf-8
import logging
import sys

import elasticsearch
from elasticsearch import ElasticsearchException
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from xylose.scielodocument import Article, Journal

ALLOWED_DOC_TYPES_N_FACETS = {
    'articles': [
        'collection',
        'subject_areas',
        'languages',
        'aff_countries',
        'publication_year',
        'document_type',
        'issn',
        'pid',
        'access_date',
        'access_year'
    ]
}


def construct_aggs(aggs, size=0):
    """
    Construct the ElasticSearch aggretions query according to a list of
    parameters that must be aggregated.
    """

    data = {}
    point = None

    def join(field, point=None):
        default = {
            field: {
                "terms": {
                    "field": field,
                    "size": 0
                },
                "aggs": {
                    "access_total": {
                        "sum": {
                            "field": "access_total"
                        }
                    }
                }
            }
        }

        if point:
            point['aggs'].setdefault(field, default[field])
            return point['aggs'][field]
        else:
            data.setdefault('aggs', default)
            return data['aggs'][field]

    for item in aggs:
        point = join(item, point=point)

    return data


def stats(*args, **kwargs):

    if 'hosts' not in kwargs:
        kwargs['hosts'] = ['127.0.0.1']

    kwargs['timeout'] = kwargs.get('timeout', 60)

    st = Stats(*args, **kwargs)

    return st


class ServerError(Exception):

    def __init__(self, value):
        self.message = 'Server Error: %s' % str(value)

    def __str__(self):
        return repr(self.message)


class Stats(Elasticsearch):

    def _query_dispatcher(self, *args, **kwargs):

        try:
            data = self.search(*args, **kwargs)
        except elasticsearch.SerializationError as e:
            logging.exception(e)
            raise e
        except elasticsearch.TransportError as e:
            logging.exception(e)
            raise e
        except elasticsearch.ConnectionError as e:
            logging.exception(e)
            raise e
        except Exception as e:
            logging.exception(e)
            raise e

        return data

    def access_search(self, parameters):

        parameters['index'] = 'accesses'
        query_result = self._query_dispatcher(**parameters)

        return query_result

    def document(self, code, collection):

        body = {
            "query": {
                "bool": {
                    "must": [{
                            "match": {
                                "pid": code
                            }
                        },
                        {
                            "match": {
                                "collection": collection
                            }

                        }

                    ]
                }
            },
            "aggs": {
                "access_total": {
                    "sum": {
                        "field": "access_total"
                    }
                },
                "access_html": {
                    "sum": {
                        "field": "access_html"
                    }
                },
                "access_pdf": {
                    "sum": {
                        "field": "access_pdf"
                    }
                },
                "access_abstract": {
                    "sum": {
                        "field": "access_abstract"
                    }
                },
                "access_epdf": {
                    "sum": {
                        "field": "access_epdf"
                    }
                }
            }
        }

        query_result = self._query_dispatcher(
            index='accesses',
            doc_type='articles',
            body=body,
            size=0
        )

        response = query_result['aggregations']

        return response

    def access_stats(self, doc_type, aggs, filters=None):

        if not aggs:
            raise ValueError(
                u'Aggregation not allowed, %s, expected %s' % (
                    str(aggs),
                    str(ALLOWED_DOC_TYPES_N_FACETS[doc_type])
                )
            )

        if doc_type not in ALLOWED_DOC_TYPES_N_FACETS.keys():
            raise ValueError(
                u'DocumentType not allowed, %s, expected %s' % (
                    doc_type,
                    str(ALLOWED_DOC_TYPES_N_FACETS.keys())
                )
            )

        for agg in aggs:
            if agg not in ALLOWED_DOC_TYPES_N_FACETS[doc_type]:
                raise ValueError(
                    u'Aggregation not allowed, %s, expected %s' % (
                        aggs,
                        str(ALLOWED_DOC_TYPES_N_FACETS[doc_type])
                    )
                )

        body = {
            "query": {
                "match_all": {}
            }
        }

        body.update(construct_aggs(aggs))

        if filters:
            must_terms = []
            for param, value in filters.items():
                if param not in ALLOWED_DOC_TYPES_N_FACETS[doc_type]:
                    raise ValueError(
                        u'Filter not allowed, %s expected %s' % (
                            param,
                            str(ALLOWED_DOC_TYPES_N_FACETS[doc_type])
                        )
                    )
                must_terms.append({'term': {param: value}})

            body['query'] = {
                "bool": {
                    "must": must_terms
                }
            }

        query_result = self._query_dispatcher(
            index='accesses',
            doc_type=doc_type,
            search_type='count',
            body=body
        )

        response = query_result['aggregations']

        return response
