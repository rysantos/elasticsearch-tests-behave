"""
Defines the steps taken to perform integration tests on the elastic heartbeat service
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *
from elasticsearch_dsl import Index, connections, Text, Document, Search
from func_timeout import func_timeout, FunctionTimedOut
import time
import uuid
from datetime import datetime, timedelta
from Tests.utils.ElasticInterface.index_interface import IndexInterface

@when('I retrieve the heartbeat logs from the last 3 minutes')
def step_impl(context):
    elastic = IndexInterface("heartbeat-*", "3m")
    lst = elastic.get_logs()
    context.result = lst

@when('I retrieve the two most recent heartbeat logs')
def step_impl(context):
    elastic = IndexInterface("heartbeat-*", "3m")
    lst = elastic.get_topTwoLogs()
    context.result = lst

@then('I should expect to see heartbeat logs')
def step_impl(context):
    assert(context.result != None)
    assert(len(context.result) > 0)

@then('I should expect to see heartbeats about 10 secounds apart')
def step_impl(context):
    heartbeat1TimeStamp = context.result[0]['@timestamp']
    heartbeat2TimeStamp = context.result[1]['@timestamp']

    date_time_obj1 = datetime.strptime(heartbeat1TimeStamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    date_time_obj2 = datetime.strptime(heartbeat2TimeStamp, '%Y-%m-%dT%H:%M:%S.%fZ')
    diff=date_time_obj1-date_time_obj2
    seconds = diff.total_seconds()
    assert(seconds > 9)
    assert(seconds < 11)