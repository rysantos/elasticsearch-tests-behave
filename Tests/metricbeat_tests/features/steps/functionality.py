"""
Defines the steps taken to perform integration tests on the metricbeat service
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *
from elasticsearch_dsl import Index, connections, Text, Document, Search
from func_timeout import func_timeout, FunctionTimedOut
import time
import uuid
from datetime import datetime, timedelta
from Tests.utils.ElasticInterface.index_interface import IndexInterface

@when('I retrieve the most recent {metric} metric logs')
def step_impl(context, metric):
    elastic = IndexInterface("metricbeat-*")
    logs = elastic.get_logs()
    lst = list()
    for hit in logs:
        res = hit.to_dict()
        if res["metricset"]["name"] == metric and res["service"]["type"] == context.module:
            lst.append(res)
    context.result = lst

@then('I should expect to see {metric} logs')
def step_impl(context, metric):
    assert(context.result != None)
    assert(len(context.result) > 0)

@then('I should expect to see {metric} metric logs about 10 secounds apart')
def step_impl(context, metric):
    lst = context.result
    diff = get_TimeDifference(lst[0]['@timestamp'],lst[1]['@timestamp'] )
    count = 1
    while diff < 1:
        #Metrics might be sent in batches
        diff = get_TimeDifference(lst[count]['@timestamp'],lst[count+1]['@timestamp'] )
        count += 1
    assert(diff > 9)
    assert(diff < 11)
    print("Passed: ", metric)

def get_TimeDifference(timestamp1, timestamp2):
    """
        Gets the Difference between two timestamps in the form of strings
        Args: Timestamp1
              Timestamp2
    """
    date_time_obj1 = datetime.strptime(timestamp1, '%Y-%m-%dT%H:%M:%S.%fZ')
    date_time_obj2 = datetime.strptime(timestamp2, '%Y-%m-%dT%H:%M:%S.%fZ')
    diff=date_time_obj1-date_time_obj2
    seconds = diff.total_seconds()
    return seconds


