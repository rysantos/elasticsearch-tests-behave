Feature: Testing the data integrity of the filebeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-FileBeat-Service_integrity-tests_test1
Scenario: Verify that the metricbeat <Module>: <Metric> is sending valid data values
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search 
    When I create a log file
    Then I should expect to not see any null values in the index

@TestCase=Elastic-FileBeat-Service_integrity-tests_test2
Scenario: Verify that the filebeat is sending timestamp data
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search 
    When I create a log file
    Then I should expect to see a timestamp field in the index

@TestCase=Elastic-FileBeat-Service_integrity-tests_test3
Scenario: Verify that the index is recieving indices from a filebeat service
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search 
    When I create a log file
    Then I should expect to see a agent.type field in the response with a value of filebeat

@TestCase=Elastic-FileBeat-Service_integrity-tests_test4
Scenario: Verify that the filebeat is running version 7.3.1
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search 
    When I create a log file
    Then I should expect to see a agent.version field in the response with a value of 7.3.1

@TestCase=Elastic-FileBeat-Service_integrity-tests_test5
Scenario: Verify that the filebeat is keeping log naming consistent
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search 
    When I create a log file
    Then I should expect to see my log file has the same name