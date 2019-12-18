"""
Defines the steps taken to perform integration tests on the filebeat service
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *
from elasticsearch_dsl import Index, connections, Text, Document, Search
from func_timeout import func_timeout, FunctionTimedOut
import time
import uuid
import sys
from datetime import datetime, timedelta
from Tests.utils.ElasticInterface.index_interface import IndexInterface

@when(u'I retrive the packetbeat logs from the last 60 seconds')
def step_impl(context):
    index = context.config.userdata.get("packetbeatOutput")
    elastic = IndexInterface(index, "60s")
    logs = elastic.get_logs()
    context.result = logs

@when(u'I make an {protocol} request')
def step_impl(context, protocol):
    pass
    #raise NotImplementedError(u'STEP: When I make a {0} request'.format(protocol))

@then(u'I should expect to see packetbeat logs')
def step_impl(context):
    logs = context.result
    assert(len(logs) > 0)

@then(u'I should expect to see the {protocol} transactions in the logs')
def step_impl(context, protocol):
    index = context.config.userdata.get("packetbeatOutput")
    elastic = IndexInterface(index, "15s")
    logs = elastic.get_logs()
    context.result = logs
    lst = list()
    for hit in logs:
        res = hit.to_dict()
        if res["type"] == protocol:
            lst.append(res)
    assert(len(lst) > 0)