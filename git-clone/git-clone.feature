Feature: Git Clone Task


    Scenario: Successfully clone a Git repository
        Given a Tekton Task definition for git clone
        When I run the PipelineRun that uses this Task
        Then the repository should be cloned to the specific directory
        And the correct revision should be checkout out
