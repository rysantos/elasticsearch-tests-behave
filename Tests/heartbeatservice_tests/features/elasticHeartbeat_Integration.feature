Feature: Testing the functionality of the heartbeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-Heartbeat-Service_integration-tests_test1
Scenario: Verify that the heartbeat is sending data
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve the heartbeat logs from the last 3 minutes
    Then I should expect to see heartbeat logs

@TestCase=Elastic-Heartbeat-Service_integration-tests_test2
Scenario: Verify that the heartbeat service is sending a heartbeat every 10 seconds 
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve the two most recent heartbeat logs
    Then I should expect to see heartbeats about 10 secounds apart