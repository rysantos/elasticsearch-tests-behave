"""
Defines steps take to perform data integrity tests on the elastic heartbeat service
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *
from elasticsearch_dsl import Index, connections, Text, Document, Search
from func_timeout import func_timeout, FunctionTimedOut
import time
import uuid
import json
from datetime import datetime, timedelta
from dateutil.parser import parse
from Tests.utils.ElasticInterface.index_interface import IndexInterface

@when('I retrieve a heartbeat log')
def step_impl(context):
    elastic = IndexInterface("heartbeat-*", "3m")
    log = elastic.get_LatestLog()
    context.result = log

@then('I should expect to not see any null values in the response')
def step_impl(context):
    response = context.result.to_dict()
    checkValues = iterate(response)
    assert(checkValues == True)

def iterate(dictionary):
    """
    Iterates through a Json object as a dictionary. 
    Returns if any field has null values

    :param dictionary: JSON object as a dictionary
    """
    for key, value in dictionary.items():
        if isinstance(value, dict):
            #print('key {!r} -> value {!r}'.format(key, value)) 
            valueCheck = iterate(value)
            if(valueCheck == False):
                return False
            continue
        else:
            #print('key {!r} -> value {!r}'.format(key, value))
            if(value == None):
                return False
    return True
    

@then('I should expect to see a timestamp field in the response')
def step_impl(context):
    response = context.result['@timestamp']
    isDate = is_date(response)
    assert(isDate == True)

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

@then('I should expect to see a agent.type field in the response with a value of heartbeat')
def step_impl(context):
    response = context.result['agent']['type']
    assert( response == "heartbeat")

@then('I should expect to see a agent.version field in the response with a value of 7.3.1')
def step_impl(context):
    response = context.result['agent']['version']
    assert( response == "7.3.1")

@then('I should expect to see a url.full field in the response with the correct url')
def step_impl(context):
    response = context.result['url']['full']
    assert( response == "http://elasticsearch:9200")

@then('I should expect to see a response code field in the response with a 200 status')
def step_impl(context):
    response = context.result['http']['response']['status_code']
    assert( response == 200)

@then('I should expect to see a total time field in the response with a value greater than 0')
def step_impl(context):
    response = context.result['http']['rtt']['total']['us']
    assert( response > 0)
