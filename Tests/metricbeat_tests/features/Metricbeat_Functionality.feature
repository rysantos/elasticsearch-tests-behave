Feature: Testing the functionality of the metricbeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-MetricBeat-Service_Functionality-tests_test1
Scenario Outline: Verify that the metricbeat is sending data for each metric in <Module>
    Given I have an elastic search cluster running
    And I have a metricbeat service running on the elastic search cluster
    And the metricbeat service is logging <Module>: <Metric>
    When I retrieve the most recent <Metric> metric logs
    Then I should expect to see <Metric> logs

Examples: Metrics
    | Module | Metric          |
    | system | cpu             |
    | system | filesystem      |
    | system | fsstat          |
    | system | load            |
    | system | memory          |
    | system | process         |
    | system | process_summary |
    | system | uptime          |
    | system | core            |
    | system | diskio          |

@TestCase=Elastic-MetricBeat-Service_Functionality-tests_test2
Scenario Outline: Verify that the metricbeat service is sending metrics for <Module>: <Metric> every 10 seconds 
    Given I have an elastic search cluster running
    And I have a metricbeat service running on the elastic search cluster
    And the metricbeat service is logging <Module>: <Metric>
    When I retrieve the most recent <Metric> metric logs
    Then I should expect to see <Metric> metric logs about 10 secounds apart

Examples: Metrics
    | Module | Metric          |
    | system | cpu             |
    | system | filesystem      |
    | system | fsstat          |
    | system | load            |
    | system | memory          |
    | system | process         |
    | system | process_summary |
    | system | uptime          |
    | system | core            |
    | system | diskio          |