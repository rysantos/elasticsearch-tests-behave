"""
Defines the Client class used to interface with Azure Dev Ops
"""
from azure.devops.connection import Connection
from azure.devops.v5_1.test_plan.models import (
    TestPlanCreateParams,
    TestSuiteCreateParams,
    TestSuiteReference,
    SuiteTestCaseCreateUpdateParameters,
    Configuration,
    WorkItem,
    TestPlan,
    TestSuite)
from azure.devops.v5_1.work_item_tracking.models import JsonPatchOperation
from msrest.authentication import BasicAuthentication
from enum import Enum
from Tests.utils.azure_devops.test_step import TestStepCollection
from typing import Iterable


class TestClient():
    """A facade on top of the azure dev ops python api
        which makes operations simpler to perform
    """

    def __init__(self, org_url: str, pat: str, project: str):
        """
        Args:
            org_url: The url of your azure dev ops organization.
            pat: An azure dev ops personal access token which has read and write access to 
                work items and the testing api.
            project: The name of the azure dev ops project the test client should target.
        """
        creds = BasicAuthentication('', pat)
        conn = Connection(org_url, creds)

        self._test_client = conn.clients_v5_1.get_test_plan_client()
        self._work_item_client = conn.clients_v5_1.get_work_item_tracking_client()
        self._project = project

    def generateTestCase(self, scenario, featureName: str):
        """
            Ensures that scenarios tagged with @TestCase= have
            matching test suites/plans/cases in azure dev ops and creates them 
            if they don't exist
            Args:
                scenario: the scenario of the test feature
                featureName: the feature name in string form
        """
        tag = self.getTestTag(scenario.tags)
        if tag is None:
            return

        plan = self.create_or_get_plan(tag[0])

        suite = self.create_or_get_suite(
            plan.id, tag[1])

        then = [x.name for x in scenario.steps if x.step_type == 'then']

        thenStmnt = ';'.join(then)

        col = TestStepCollection()

        for step in scenario.steps:
            if step.step_type == 'given':
                col.add_test_step(step.name)
            if step.step_type == 'when':
                col.add_test_step(step.name, thenStmnt)

        self.create_or_get_tc(plan.id, suite.id, tag[2], col, featureName)

    def getTestTag(self, tags):
        """Parses the test tag into a list of strings

            Args:
                tags (list<str>): a list of all the tags on a scenario

            Returns:
                A list of strings with the TestCase tag split into individual parts: (test plan, test suite, test case)
        """
        tag = next((t for t in tags if "TestCase=" in t), None)
        if tag is None:
            return None

        _, _, testInfo = tag.partition('=')
        return testInfo.split("_")

    def create_or_get_plan(self, plan_name: str) -> TestPlan:
        """Retrieves a test plan or creates it if it doesn't exist.

            When a test plan is created in azure devops 
                a root level test suite with the same name is also automatically created

            Args:
                plan_name: Name of the test plan.

            Returns:
                The test plan that was created or retrieved
        """
        for plans in self.get_plans():
            plan = next(
                (p for p in plans if p.name == plan_name), None)

            if plan is not None:
                return plan

        return self._test_client.create_test_plan(
            TestPlanCreateParams(name=plan_name), self._project)

    def get_plans(self) -> Iterable[TestPlan]:
        """Gets all the test plans for a project

            Returns:
                An iterable of test plans
        """
        plan_response = self._test_client.get_test_plans(self._project)

        while True:
            yield plan_response.value

            if not plan_response.continuation_token:
                return

            plan_response = self._test_client.get_test_plans(
                self._project, continuation_token=plan_response.continuation_token)

    def create_or_get_suite(self, plan_id: int, suite_name: str) -> TestSuite:
        """Retrieves a test suite or creates it if it doesn't exist.

            Args:
                plan_id: Id of the test plan to which the suite belongs.
                suite_name: The name of the test suite

            Returns:
                The retrieved or created test suite
        """
        parent_suite = None

        for idx, suites in enumerate(self.get_suites(plan_id)):
            # First plan will be the default one created by azure dev ops
            # when the test suite is created
            if idx == 0:
                parent_suite = suites[0]

            suite = next(
                (s for s in suites if s.name == suite_name), None)

            if suite is not None:
                return suite

        # Test suites cannot be created without a referenced parent suite
        # The required parameter options may be different based on the the ssuite type
        # requirement_id reqired for RequirementTestSuite
        # query required for DynamicTestSuite
        params = TestSuiteCreateParams(name=suite_name, parent_suite=TestSuiteReference(
            id=parent_suite.id), suite_type=TestSuiteType.StaticTestSuite.name)

        result = self._test_client.create_test_suite(
            params, self._project, plan_id)

        return result

    def get_suites(self, plan_id: int) -> Iterable[TestSuite]:
        """Gets all the test suites for a plan

            Args:
                plan_id: Id of the test plan to which the suite belongs.

            Returns:
                An iterable of test suites
        """
        suite_response = self._test_client.get_test_suites_for_plan(
            self._project, plan_id)

        while True:
            yield suite_response.value

            if not suite_response.continuation_token:
                return

            suite_response = self._test_client.get_test_suites_for_plan(
                self._project, plan_id, continuation_token=suite_response.continuation_token)

    def create_or_get_tc(self, plan_id: int, suite_id: str, tc_name: str, test_step_collection: TestStepCollection, test_feature: str) -> WorkItem:
        """Retrieves a test case or creates it if it doesn't exist.

            Args:
                plan_id: Id of the test plan to which the tc belongs.
                suite_id: Id of the test suite to which the tc belongs.
                test_step_collection: A test step collection to upload if 
                    a new tc is created. This argument will be ignored if the tc already exists.
                test_feature: The feature that the test case is identifying

            Returns:
                The created or retrieved work item
        """
        for tcs in self.get_tcs(plan_id, suite_id):
            tc = next(
                (t for t in tcs if t.work_item.name == tc_name), None)

            if tc is not None:
                work_item = self.update_tc(tc.work_item.id, test_step_collection, test_feature)
                return tc

        work_item = self.create_tc(tc_name, test_step_collection, test_feature)

        result = self._test_client.add_test_cases_to_suite(
            [SuiteTestCaseCreateUpdateParameters([], WorkItem(work_item.id))], self._project, plan_id, suite_id)

        return next((t for t in result if t.work_item.name == tc_name)).work_item

    def get_tcs(self, plan_id: int, suite_id: int) -> Iterable[WorkItem]:
        """Gets all the test cases for a plan and suite

            Args:
                plan_id: Id of the test plan to which the tc belongs.
                suite_id: Id of the test suite to which the tc belongs.

            Returns:
                An iterable of eork items
        """
        tc_response = self._test_client.get_test_case_list(
            self._project, plan_id, suite_id)

        while True:
            yield tc_response.value

            if not tc_response.continuation_token:
                return

            tc_response = self._test_client.get_test_case_list(self._project, plan_id, suite_id,
                                                               continuation_token=tc_response.continuation_token)

    def create_tc(self, tc_name: str, test_step_collection: TestStepCollection, test_feature) -> WorkItem:
        """Creates a new test case

            Args:
                tc_name: Name of the test case to create
                test_step_collection: The collection of test steps to add to the test case.
                test_feature: The feature that a test is identifying

            Returns:
                The created work item
        """
        ops = [JsonPatchOperation(op="add", path="/fields/System.Title", value=tc_name),
               JsonPatchOperation(op="add", path="/fields/Microsoft.VSTS.TCM.Steps", value=test_step_collection.serialize()),
               JsonPatchOperation(op="add", path="/fields/System.Description", value=test_feature)]

        return self._work_item_client.create_work_item(ops, self._project, "Test Case")

    def update_tc(self, tc_id: str, test_step_collection: TestStepCollection, test_feature) -> WorkItem:
        """Updates the old test case

            Args:
                tc_id: Id of the test case to be updated
                test_step_collection: The collection of test steps to add to the test case.
                test_feature: The feature that a test is identifying
        """
        ops = [
            JsonPatchOperation(op="add", path="/fields/Microsoft.VSTS.TCM.Steps", value=test_step_collection.serialize()),
            JsonPatchOperation(op="add", path="/fields/System.Description", value=test_feature)]

        return self._work_item_client.update_work_item(ops, tc_id)

class TestSuiteType(Enum):
    """Represents the different test suite types supported by azure dev ops"""
    RequirementTestSuite = 0
    DynamicTestSuite = 1
    StaticTestSuite = 2