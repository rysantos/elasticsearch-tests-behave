Feature: Testing the data integrity of the heartbeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-Heartbeat-Service_integrity-tests_test1
Scenario: Verify that the heartbeat is sending valid data values
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve a heartbeat log
    Then I should expect to not see any null values in the response

@TestCase=Elastic-Heartbeat-Service_integrity-tests_test2
Scenario: Verify that the heartbeat is sending timestamp data
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve a heartbeat log
    Then I should expect to see a timestamp field in the response

@TestCase=Elastic-Heartbeat-Service_integrity-tests_test3
Scenario: Verify that the heartbeat is in fact a heartbeat service
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve a heartbeat log
    Then I should expect to see a agent.type field in the response with a value of heartbeat

@TestCase=Elastic-Heartbeat-Service_integrity-tests_test4
Scenario: Verify that the heartbeat is running version 7.3.1
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve a heartbeat log
    Then I should expect to see a agent.version field in the response with a value of 7.3.1

@TestCase=Elastic-Heartbeat-Service_integrity-tests_test5
Scenario: Verify that the heartbeat is sending a request to the correct url
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve a heartbeat log
    Then I should expect to see a url.full field in the response with the correct url

@TestCase=Elastic-Heartbeat-Service_integrity-tests_test6
Scenario: Verify that the heartbeat is recieving a 200 status code
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve a heartbeat log
    Then I should expect to see a response code field in the response with a 200 status

@TestCase=Elastic-Heartbeat-Service_integrity-tests_test7
Scenario: Verify that the heartbeat is sending a valid time to retrieve content value
    Given I have an elastic search cluster running
    And I have a heartbeat servie running on the elastic search cluster
    When I retrieve a heartbeat log
    Then I should expect to see a total time field in the response with a value greater than 0