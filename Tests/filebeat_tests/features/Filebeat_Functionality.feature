Feature: Testing the functionality of the filebeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-FileBeat-Service_Functionality-tests_test1
@logstash
Scenario: Verify that the filebeat is sending log data for new log files
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search 
    When I create a log file
    Then I should expect to see that log file in the specified index

@TestCase=Elastic-FileBeat-Service_Functionality-tests_test2
@logstash
Scenario: Verify that the filebeat is sending log data on truncated log files
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search
    And a log file is already uploaded
    When I truncate the log file
    Then I should expect to see my changes to the log file in the specified index

@TestCase=Elastic-FileBeat-Service_Functionality-tests_test3
@logstash
Scenario: Verify that the filebeat is sending log data on appended log files
    Given I have an elastic search cluster running
    And I have a filebeat service running
    And the filebeat service is monitoring log files
    And the filebeat service is sending output to elastic search 
    And a log file is already uploaded
    When I append to the log file
    Then I should expect to see my changes to the log file in the specified index