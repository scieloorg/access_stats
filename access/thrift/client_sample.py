# coding: utf-8
import os
import thriftpy
import json
from thriftpy.rpc import make_client

access_stats_thrift = thriftpy.load(
    os.path.dirname(__file__)+'/access_stats.thrift',
    module_name='access_stats_thrift'
)

if __name__ == '__main__':

    client = make_client(
        access_stats_thrift.AccessStats,
        'localhost',
        11660
    )

    #print(json.loads(client.document('S1807-86212013000200003', 'scl')))

    query_parameters = [
        access_stats_thrift.kwargs('size', '0')
    ]

    print(json.loads(client.search('{}', query_parameters)))
