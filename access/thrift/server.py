# coding: utf-8
import json
import argparse
import logging
import os
import sys

from access.controller import stats, ServerError

import thriftpy
import thriftpywrap
from thriftpy.rpc import make_server

logger = logging.getLogger(__name__)

access_stats_thrift = thriftpy.load(
    os.path.join(os.path.dirname(__file__), 'access_stats.thrift'))


class Dispatcher(object):

    def __init__(self):

        self._stats = stats()

    def _stats_dispatcher(self, *args, **kwargs):

        try:
            data = self._stats.access_stats(*args, **kwargs)
        except ValueError as e:
            logging.error(e.message)
            raise access_stats_thrift.ValueError(message=e.message)
        except ServerError as e:
            raise access_stats_thrift.ServerError(message=e.message)

        return data

    def search(self, body, parameters):

        params = {i.key:i.value for i in parameters}
        params['doc_type'] = 'articles'
        params['body'] = json.loads(body)

        try:
            data = self._stats.access_search(params)
        except ValueError as e:
            logging.error(e.message)
            raise access_stats_thrift.ValueError(message=e.message)
        except ServerError as e:
            raise access_stats_thrift.ServerError(message=e.message)

        try:
            data_str = json.dumps(data)
        except ValueError as e:
            logging.error('Invalid JSON data: %s' % data_str)
            raise access_stats_thrift.ValueError(message=e.message)

        return data_str

    def document(self, code, collection):

        try:
            data = self._stats.document(code, collection)
        except ValueError as err:
            raise access_stats_thrift.ServerError(
                'Fail to retrieve data from server: %s' % err.message
            )

        result = json.dumps(data)

        return result

main = thriftpywrap.ConsoleApp(access_stats_thrift.AccessStats, Dispatcher)
