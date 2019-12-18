Feature: Test sending telemetry data to Elastic Search
Author: rysantos@microsoft.com

@TestCase=Regression-Git_Plan-Git_test1-1234
Scenario: Test sending 10 messages from a file to elastic Search
    Given I have an elastic search cluster running in a docker container
    And I have a flat file with 10 messages in it
    When I execute the telemetry harness
    Then I should expect to see 10 messages in elastic 