"""
Defines commons test steps that are shared among features and scenarios
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *

@given('I have an elastic search cluster running')
def step_impl(context):
    pass

@given('I have a heartbeat servie running on the elastic search cluster')
def step_impl(context):
    pass 