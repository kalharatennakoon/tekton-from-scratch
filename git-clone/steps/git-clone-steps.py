from behave import given, when, then
import subprocess
import os
import yaml


# Define the paths to your Tekton Task, Pipeline, and PipelineRun files
task_file = "./git-clone-task.yaml"
pipeline_file = "./git-clone-pipeline.yaml"
pipelinerun_file = "./git-clone-pipelinerun.yaml"

@given('a Tekton Task definition for git clone')
def step_given_tekton_task(context):
    with open(task_file, 'r') as file:
        context.file = yaml.safe_load(file)
    assert context.file is not None


@when('I run the PipelineRun that uses this Task')
def step_when_run_pipelinerun(context):
    # Apply the Task, Pipeline, and PipelineRun using kubectl or tkn
    subprocess.run(["kubectl", "apply", "-f", task_file], check=True)
    subprocess.run(["kubectl", "apply", "-f", pipeline_file], check=True)
    subprocess.run(["kubectl", "apply", "-f", pipelinerun_file], check=True)

    # Wait for the PipelineRun to complete (You may want to poll the status)
    context.result = subprocess.run(
        ["tkn", "pipelinerun", "logs", "git-clone-pipelinerun", "-f"],
        capture_output=True, text=True, check=True
    ).stdout


@then('the repository should be cloned to the specific directory')
def step_then_verify_clone(context):
    clone_dir = "/workspace/repo"
    assert os.path.exists(clone_dir), "Repository directory does not exist"


@then('the correct revision should be checkout out')
def step_then_verify_revision(context):
    clone_dir = "/workspace/repo"
    os.chdir(clone_dir)
    result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    branch = result.stdout.strip()
    assert branch == "main", f"Expected branch 'main' but got '{branch}'"
