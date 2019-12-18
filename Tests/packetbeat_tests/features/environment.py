"""
Defines code to run before and after certain events during testing
"""
import sys
import os
from behave import fixture, use_fixture
from elasticsearch_dsl import Index, connections, Text, Document, Search

sys.path.append('../../')
from Tests.utils.azure_devops.test_client import TestClient

@fixture
def elastic_search(context):
    """Behave Fixture method.

        Sets up elastic search connection and makes sure our index is available.
    """    
    print("Setting up Elastic Search")
    userdata = context.config.userdata
    authentication = userdata.get("esUser") + ":" + userdata.get("esPassword")
    connections.create_connection(hosts=[userdata.get("esHost")], http_auth=(authentication), timeout=20)

def before_all(context):
    """Behave lifecycle method

        Callas the elastic search fixture
    """
    use_fixture(elastic_search, context)

def before_feature(context, feature):
    """Behave lifecycle method

        Parses the feature into a string 
    """
    context.test_feature = feature.name

def before_scenario(context, scenario):
    """Behave lifecycle method

        Checks our behave userdata for ADO credentials.
        If we have credentials we call our ADO TestClient 
        to create a test case for the scenario
    """
    userdata = context.config.userdata
    org = userdata.get("devopsOrgUrl")
    pat = userdata.get("personalAccessToken")
    project = userdata.get("devopsProjectName")
    if( org != None) and (len(org)>0) and (pat != None) and (len(pat)>0) and (project != None) and (len(project)>0):
        client = TestClient(org, pat, project)
        client.generateTestCase(scenario, context.test_feature)