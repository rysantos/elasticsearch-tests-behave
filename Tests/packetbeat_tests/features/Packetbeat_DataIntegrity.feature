Feature: Testing the data integrity of the packetbeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-PacketBeat-Service_integrity-tests_test1
Scenario Outline: Verify that the packetbeat service is sending valid data values
    Given I have an elastic search cluster running
    And I have a packetbeat service running
    And the packetbeat service is monitoring <Protocol> transactions
    When I make an <Protocol> request
    Then I should expect to not see any null values for <Protocol> in the index

Examples: Protocols
    | Protocol  |
    | flow      |
    | dns       |
    | http      |
    | redis     |
    | mongodb   |