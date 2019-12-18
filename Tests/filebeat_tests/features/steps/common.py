"""
Defines commons test steps that are shared among features and scenarios
"""
# pylint: disable=function-redefined,undefined-variable
import time
import sys
from behave import *
from shutil import copyfile


@given('I have an elastic search cluster running')
def step_impl(context):
    pass

@given('I have a filebeat service running')
def step_impl(context):
    pass 

@given('the filebeat service is monitoring log files')
def step_impl(context):
    pass 

@given('the filebeat service is sending output to elastic search')
def step_impl(context):
    pass

@given(u'a log file is already uploaded')
def step_impl(context):
    copyFile(context)
    waitForFilebeat(context)

@when('I create a log file')
def step_impl(context):
    copyFile(context)
    readFileContents(context)
    waitForFilebeat(context)

def copyFile(context):
    """
        Copies the log file for this test suite to the filebeat log directory specified in the behave.ini
    """
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    fileLocation = context.config.userdata.get("logFile")
    try:
        copyfile(fileLocation, logDirectory)
    except IOError as e:
        print("Unable to copy file. %s" % e)
        raise e
    except:
        print("Unexpected error:", sys.exc_info())
        raise e
    print("Creating File")

def readFileContents(context):
    """
        Reads file contents into the context.results field to be asserted on later
    """
    logDirectory = context.config.userdata.get("filebeatLogsDirectory")
    with open(logDirectory, "r") as f:
        try:
            context.results = f.readlines()
        except IOError as e:
            print("Unable to copy file. %s" % e)
            raise e
        except:
            print("Unexpected error:", sys.exc_info())
            raise e

def waitForFilebeat(context):
    """
        Filebeat has a delay when it recognizes changes to files. We have to give it time to see our change
    """
    latency = int(context.config.userdata.get("filebeatLatency"))
    i=1
    print("Waiting for file beat ")
    while i <= latency:
        time.sleep(1)
        i +=1
        print('.',end='',flush=True)
    print('\n',end='',flush=True)
