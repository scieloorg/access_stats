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
            logger.error(e.message)
            raise access_stats_thrift.ValueError(e.message)
        except ServerError as e:
            logger.exception(e)
            raise access_stats_thrift.ServerError('Unknow Server Error')
        except Exception as e:
            logger.exception(e)
            raise access_stats_thrift.ServerError('Unknow Server Error')

        return data

    def search(self, body, parameters):

        if parameters:
            params = {i.key:i.value for i in parameters}
        else:
            params = {}

        params['doc_type'] = 'articles'

        params['body'] = json.loads(body)

        try:
            data = self._stats.access_search(params)
        except ValueError as e:
            logger.error(e.message)
            raise access_stats_thrift.ValueError(e.message)
        except access_stats_thrift.ServerError as e:
            logger.error(e)
            raise access_stats_thrift.ServerError('Unknow Server Error')
        except Exception as e:
            logger.error(e)
            raise access_stats_thrift.ServerError('Unknow Server Error')


        try:
            data_str = json.dumps(data)
        except ValueError as e:
            logger.error('Invalid JSON data: %s' % data_str)
            raise access_stats_thrift.ValueError(str(e))

        return data_str

    def document(self, code, collection):

        try:
            data = self._stats.document(code, collection)
        except ValueError as err:
            logger.error('Server Error: %s' % data_str)
            raise access_stats_thrift.ServerError(
                'Fail to retrieve data from server: %s' % err.message
            )
        except access_stats_thrift.ServerError as e:
            logger.exception(e)
            raise access_stats_thrift.ServerError('Unknow Server Error')
        except Exception as e:
            logger.exception(e)
            raise access_stats_thrift.ServerError('Unknow Server Error')

        result = json.dumps(data)

        return result

main = thriftpywrap.ConsoleApp(access_stats_thrift.AccessStats, Dispatcher)
