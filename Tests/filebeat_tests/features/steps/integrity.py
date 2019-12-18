"""
Defines steps take to perform data integrity tests on the filebeat beat service
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *
from elasticsearch_dsl import Index, connections, Text, Document, Search
from func_timeout import func_timeout, FunctionTimedOut
import time
import uuid
import json
import sys
import ntpath
from datetime import datetime, timedelta
from dateutil.parser import parse
from shutil import copyfile
from Tests.utils.ElasticInterface.index_interface import IndexInterface
from Tests.filebeat_tests.features.steps.common import waitForFilebeat

@then(u'I should expect to not see any null values in the index')
def step_impl(context):
    index = context.config.userdata.get("filebeatOutput")
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    filename = ntpath.basename(logDirectory)
    elastic = IndexInterface(index)
    logs = elastic.get_logs()
    lst = list()
    for hit in logs:
        res = hit.to_dict()
        if res["log"]["file"]["path"] == "/var/log/"+filename:
            lst.append(res)
    for item in lst:
        assert(iterate(item))
    
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

@then(u'I should expect to see a timestamp field in the index')
def step_impl(context):
    index = context.config.userdata.get("filebeatOutput")
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    filename = ntpath.basename(logDirectory)
    elastic = IndexInterface(index)
    logs = elastic.get_logs()
    lst = list()
    for hit in logs:
        res = hit.to_dict()
        if res["log"]["file"]["path"] == "/var/log/"+filename:
            lst.append(res)
    for item in lst:
        assert(is_date(item["@timestamp"]))

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

@then(u'I should expect to see a agent.type field in the response with a value of {name}')
def step_impl(context, name):
    index = context.config.userdata.get("filebeatOutput")
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    filename = ntpath.basename(logDirectory)
    elastic = IndexInterface(index)
    logs = elastic.get_logs()
    lst = list()
    for hit in logs:
        res = hit.to_dict()
        if res["log"]["file"]["path"] == "/var/log/"+filename:
            lst.append(res)
    for item in lst:
        assert(item["agent"]["type"] == name)

@then(u'I should expect to see a agent.version field in the response with a value of {version}')
def step_impl(context,version):
    index = context.config.userdata.get("filebeatOutput")
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    filename = ntpath.basename(logDirectory)
    elastic = IndexInterface(index)
    logs = elastic.get_logs()
    lst = list()
    for hit in logs:
        res = hit.to_dict()
        if res["log"]["file"]["path"] == "/var/log/"+filename:
            lst.append(res)
    for item in lst:
        assert(item["agent"]["version"] == version)

@then(u'I should expect to see my log file has the same name')
def step_impl(context):
    index = context.config.userdata.get("filebeatOutput")
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    fileLocation = context.config.userdata.get("logFile")
    filename = ntpath.basename(logDirectory)
    elastic = IndexInterface(index)
    logs = elastic.get_logs()
    lst = list()
    for hit in logs:
        res = hit.to_dict()
        if res["log"]["file"]["path"] == "/var/log/"+filename:
            lst.append(res)
    for item in lst:
        assert(ntpath.basename(item["log"]["file"]["path"]) == filename)