Feature: Testing the data integrity of the metricbeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-MetricBeat-Service_integrity-tests_test1
Scenario Outline: Verify that the metricbeat <Module>: <Metric> is sending valid data values
    Given I have an elastic search cluster running
    And I have a metricbeat service running on the elastic search cluster
    And the metricbeat service is logging <Module>: <Metric>
    When I retrieve a <Metric> log
    Then I should expect to not see any null values in the response

Examples: Metrics
    | Module | Metric          |
    | system |   cpu           |
    | system | filesystem      |
    | system | fsstat          |
    | system | load            |
    | system | memory          |
    | system | process         |
    | system | process_summary |
    | system | uptime          |
    | system | core            |
    | system | diskio          |

@TestCase=Elastic-MetricBeat-Service_integrity-tests_test3
Scenario Outline: Verify that the metricbeat <Module>: <Metric> is sending timestamp data
    Given I have an elastic search cluster running
    And I have a metricbeat service running on the elastic search cluster
    And the metricbeat service is logging <Module>: <Metric>
    When I retrieve a <Metric> log
    Then I should expect to see a timestamp field in the response

Examples: Metrics
    | Module | Metric          |
    | system |   cpu           |
    | system | filesystem      |
    | system | fsstat          |
    | system | load            |
    | system | memory          |
    | system | process         |
    | system | process_summary |
    | system | uptime          |
    | system | core            |
    | system | diskio          |

@TestCase=Elastic-MetricBeat-Service_integrity-tests_test4
Scenario Outline: Verify that the metricbeat <Module>: <Metric> is in fact a metricbeat service
    Given I have an elastic search cluster running
    And I have a metricbeat service running on the elastic search cluster
    And the metricbeat service is logging <Module>: <Metric>
    When I retrieve a <Metric> log
    Then I should expect to see a agent.type field in the response with a value of metricbeat

Examples: Metrics
    | Module | Metric          |
    | system |   cpu           |
    | system | filesystem      |
    | system | fsstat          |
    | system | load            |
    | system | memory          |
    | system | process         |
    | system | process_summary |
    | system | uptime          |
    | system | core            |
    | system | diskio          |

@TestCase=Elastic-MetricBeat-Service_integrity-tests_test5
Scenario Outline: Verify that the metricbeat <Module>: <Metric> is running version 7.3.1
    Given I have an elastic search cluster running
    And I have a metricbeat service running on the elastic search cluster
    And the metricbeat service is logging <Module>: <Metric>
    When I retrieve a <Metric> log
    Then I should expect to see a agent.version field in the response with a value of 7.3.1

Examples: Metrics
    | Module | Metric          |
    | system |   cpu           |
    | system | filesystem      |
    | system | fsstat          |
    | system | load            |
    | system | memory          |
    | system | process         |
    | system | process_summary |
    | system | uptime          |
    | system | core            |
    | system | diskio          |