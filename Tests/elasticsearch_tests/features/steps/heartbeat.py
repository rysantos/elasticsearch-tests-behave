"""
Defines the steps taken to determine the functionality of elastic search
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *
from elasticsearch_dsl import Index, connections, Text, Document, Search
from func_timeout import func_timeout, FunctionTimedOut
import time
import uuid
from datetime import datetime, timedelta
from Tests.elasticsearch_tests.utils.telemetry_data import TelemetryData, get_uuids, delete_uuids


@given('I have an elastic search cluster running in a docker container')
def step_impl(context):
    pass


@given('I have a flat file with 10 messages in it')
def step_impl(context):
    assert context.uuids != None


@when('I execute the telemetry harness')
def step_impl(context):
    index = context.config.userdata.get("esIndexName")
    save_uuids(context.uuids, index)


def save_uuids(uuids, index):
    for uuid in uuids:
        doc = TelemetryData(uuid=uuid)
        doc.save(index=index)


@then('I should expect to see 10 messages in elastic')
def step_impl(context):
    verified = verify_data(context)
    assert verified


def verify_data(context):
    index = context.config.userdata.get("esIndexName")
    timeout = float(context.config.userdata.get("timeoutInSec"))
    timeLimit = (datetime.now() + timedelta(seconds=timeout)).time()

    while True:
        dbuuids = get_uuids(context.uuids, index)
        print(dbuuids)
        print(context.uuids)
        if all(elem in dbuuids for elem in context.uuids):
            return True
        
        if timeLimit < datetime.now().time():
            diff = ' '.join(
                [item for item in context.uuids if item not in dbuuids])
            raise TimeoutError(
                f'Test timed out, uuids: {diff} expected but not found')

        time.sleep(0.25)

    return False
