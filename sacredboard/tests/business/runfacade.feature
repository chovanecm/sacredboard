# Created by martin at 17.9.17
Feature: Run Facade
  A business layer that handles more complex operations on experiment runs.

  Scenario: Removing a run
    Given Data gateway
    When Run 123 exists
    And Metric metric1 of run 123 exists
    And Resource r1 of run 123 exists
    And Artifact a1 of run 123 exists
    And Source s1 of run 123 exists
    And I delete run 123
    Then Run 123 should not exist
    And Metric metric1 of run 123 should not exist
    And Resource r1 of run 123 should not exist
    And Artifact a1 of run 123 should not exist
    And Source s1 of run 123 should not exist


  Scenario: Removing a run when two runs exist
    Given Data gateway
    When Run 123 exists
    And Run 456 exists
    And Metric metric1 of run 123 exists
    And Metric metric2 of run 456 exists
    And I delete run 123
    Then Run 123 should not exist
    And Metric metric1 of run 123 should not exist
    And Run 456 should exist
    And Metric metric2 of run 456 should exist

  Scenario: Removing a run with two metrics
    Given Data gateway
    When Run 123 exists
    And Run 456 exists
    And Metric metric1 of run 123 exists
    And Metric metric2 of run 123 exists
    And Metric metric3 of run 456 exists
    And I delete run 123
    Then Run 123 should not exist
    And Metric metric1 of run 123 should not exist
    And Metric metric2 of run 123 should not exist
    And Run 456 should exist
    And Metric metric3 of run 456 should exist
    And Metric metric3 of run 123 should not exist