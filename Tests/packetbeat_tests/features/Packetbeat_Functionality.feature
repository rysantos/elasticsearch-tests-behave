Feature: Testing the functionality of the packetbeat service on an Elastic Cluster
Author: rysantos@microsoft.com

@TestCase=Elastic-PacketBeat-Service_Functionality-tests_test1
Scenario: Verify that the packetbeat is sending packet data
    Given I have an elastic search cluster running
    And I have a packetbeat service running
    When I retrive the packetbeat logs from the last 60 seconds
    Then I should expect to see packetbeat logs

@TestCase=Elastic-PacketBeat-Service_Functionality-tests_test2
Scenario Outline: Verify that the packet beat is monitoring <Protocol> traffic
    Given I have an elastic search cluster running
    And I have a packetbeat service running
    And the packetbeat service is monitoring <Protocol> transactions
    When I make an <Protocol> request
    Then I should expect to see the <Protocol> transactions in the logs  

Examples: Protocols
    | Protocol  | 
    | flow       |
    | dns       |
    | http      |
    | redis     |
    | mongodb   |