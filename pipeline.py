#!/usr/bin/env python3
from ast import main
import os
import argparse

DEBUG = False

#JENKINS_SERVER = os.environ['JENKINS_SERVER']
#USER_NAME = os.environ['JENKINS_USER']
#PASSWORD = os.environ['JENKINS_PAS']


def get_project_name(argument):
    git_project_name = argument.split('/')[-1]
    project_name = git_project_name.split('.git')[0]
    return project_name


def get_job_configuration(credential_id, project_type, project_name,
                          jenkins_file="Jenkinsfile"):
    config_xml = f"""<?xml version='1.1' encoding='UTF-8'?>
<flow-definition plugin="workflow-job@1207.ve6191ff089f8">
<actions>
<org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobAction plugin="pipeline-model-definition@2.2114.v2654ca_721309"/>
<org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction plugin="pipeline-model-definition@2.2114.v2654ca_721309">
<jobProperties/>
<triggers/>
<parameters/>
<options/>
</org.jenkinsci.plugins.pipeline.modeldefinition.actions.DeclarativeJobPropertyTrackerAction>
</actions>
<description/>
<keepDependencies>false</keepDependencies>
<properties/>
<definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition" plugin="workflow-cps@2759.v87459c4eea_ca_">
<script>pipeline { agent any environment { git_commit_message = '' git_commit_diff = '' git_commit_author = '' git_commit_author_name = '' git_commit_author_email = '' } stages { // Build stage('Build') { steps { deleteDir() } } // Static Code Analysis stage('Static Code Analysis') { steps { deleteDir() sh "echo 'Run Static Code Analysis'" } } // Unit Tests stage('Unit Tests') { steps { deleteDir() sh "echo 'Run Unit Tests'" } } } }</script>
<sandbox>true</sandbox>
</definition>
<triggers/>
<disabled>false</disabled>
</flow-definition>

"""

    return config_xml


def jenkins_create_job(server, project_name, project_folder, config_xml):
    if server.job_exists(name=project_name):
        raise Exception("Pipeline with name {project_name} already exist.")

    server.create_job(name=project_folder+"/"+project_name, config_xml=config_xml)
    pass


def jenkins_info(server):
    user = server.get_whoami()
    print(f"Hello {user['fullName']} from Jenkins {server.get_version()}")

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_url", help="Repository URL")
    parser.add_argument("credential_id", help="Jenkins credential id to access"
                                              "given repository URL")
    parser.add_argument("jenkins_url", help="Jenkins URL")
    parser.add_argument("jenkins_user", help="Jenkins user")
    parser.add_argument("jenkins_password", help="Jenkins password")
    parser.add_argument("project_folder", help="Project folder")
    parser.add_argument("project_type", help="Project type")
    arguments = parser.parse_args()
    main(arguments)
