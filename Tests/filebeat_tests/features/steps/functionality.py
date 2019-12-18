"""
Defines the steps taken to perform integration tests on the filebeat service
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *
from elasticsearch_dsl import Index, connections, Text, Document, Search
from func_timeout import func_timeout, FunctionTimedOut
import time
import uuid
import ntpath
import sys
from datetime import datetime, timedelta
from shutil import copyfile
from Tests.utils.ElasticInterface.index_interface import IndexInterface
from Tests.filebeat_tests.features.steps.common import waitForFilebeat

@when(u'I append to the log file')
def step_impl(context):
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    with open(logDirectory, "a") as f:
        try:
            line = "appending a test line\n"
            f.write(line)
            context.result = line.splitlines()
        except IOError as e:
            print("Unable to copy file. %s" % e)
            raise e
        except:
            print("Unexpected error:", sys.exc_info())
            raise e
    waitForFilebeat(context)

@when(u'I truncate the log file')
def step_impl(context):
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    with open(logDirectory, "r+") as f:
        try:
            line = f.readline()
            context.result = line.splitlines()
            f.truncate(len(line)+1)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            raise e
        except:
            print("Unexpected error:", sys.exc_info())
            raise e
    waitForFilebeat(context)

@then('I should expect to see that log file in the specified index')
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
    del lst[len(context.results):]
    logLines = list()
    for item in lst:
        logLines.append(item["message"].splitlines())
    for line in context.results:
        if line.splitlines() not in logLines:
            assert(False)


@then(u'I should expect to see my changes to the log file in the specified index')
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
    message = lst[0]["message"].splitlines()
    assert(message == context.result)