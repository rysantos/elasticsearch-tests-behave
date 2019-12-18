"""
Defines commons test steps that are shared among features and scenarios
"""
# pylint: disable=function-redefined,undefined-variable

from behave import *

@given('I have an elastic search cluster running')
def step_impl(context):
    pass

@given('I have a metricbeat service running on the elastic search cluster')
def step_impl(context):
    pass 

@given('the metricbeat service is logging {module}: {metric}')
def step_impl(context,module, metric):
    context.module = module
    context.metric = metric