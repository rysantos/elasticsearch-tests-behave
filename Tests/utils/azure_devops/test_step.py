"""
Defines the TestStep class for test steps in Azure Dev Ops
"""
from enum import Enum


class TestStepType(Enum):
    """Represents the two test step types expected by azure dev ops.

        If the test step has a result field the test step type should be
            ValidateStep, otherwise the type should be ActionStep
    """
    ValidateStep = 0
    ActionStep = 1


class TestStep():
    """Represents a test step in an azure dev ops test case.

        Instead of creating TestStep objects directly, prefer to use the add_test_step
            method on the TestStepCollection.
    """

    def __init__(self, id: int, action: str, result: str = None):
        """
            Args:
                id: The 1 based index of the test step in a test step collection.
                action: A test step action the tester should take,
                    maps to the azure devops action field of the test step.
                result: An optional parameter which maps to the result 
                    field of the azure dev ops test step.
        """
        self.id = id
        self.action = action
        self.result = result
        self.type = TestStepType.ActionStep if result is None else TestStepType.ValidateStep

    def serialize(self) -> str:
        """Serializes the the test step to the xml format expected 
            by azure dev ops for uploading test steps.

            Returns:
                A serialized xml representation of the test step
        """
        stepXml = f'<step id="{self.id}" type="{self.type.name}">'
        actionXml = f'<parameterizedString isformatted="true">&lt;DIV&gt;&lt;P&gt;{self.action}&lt;/P&gt;&lt;/DIV&gt;</parameterizedString>'
        resultXml = f'<parameterizedString isformatted="true">&lt;P&gt;{self.result}&lt;/P&gt;</parameterizedString>' if self.type == TestStepType.ValidateStep else '<parameterizedString isformatted="true">&lt;DIV&gt;&lt;P&gt;&lt;BR/&gt;&lt;/P&gt;&lt;/DIV&gt;</parameterizedString>'
        descriptionXml = "<description/>"

        return ''.join([stepXml, actionXml, resultXml, descriptionXml, '</step>'])


class TestStepCollection():
    """Represents a list of test steps for an azure dev ops test case."""
    _test_steps = []

    def add_test_step(self, action: str, result: str = None):
        """Adds a test step to the collection

        Args:
            action: A test step action the tester should take,
                maps to the azure devops action field of the test step.
            result: An optional parameter which maps to the result 
                field of the azure dev ops test step.
        """
        # Test Step ID is one based
        id = len(self._test_steps) + 1

        ts = TestStep(id, action, result)
        self._test_steps.append(ts)

    def serialize(self) -> str:
        """Serializes the the test step collection to the xml format expected 
            by azure dev ops for uploading test steps.

            Returns:
                A serialized xml representation of the test collection
        """
        stepsXml = f'<steps id="0" last="{len(self._test_steps)}">'

        xml_steps = []
        for step in self._test_steps:
            xml_steps.append(step.serialize())

        return ''.join([stepsXml, *xml_steps, '</steps>'])
