# About
Rodan is a generic workflow execution system, where users can upload files (called "Resources") and define an execution chain (a "Workflow") for processing these files. Each workflow is composed of "Jobs," the functionality of which can be drawn from a shell executable or a Python library. Running a workflow will pass the resources through the chain of jobs, finishing with the output of the last job.

A unique feature of Rodan is the "Interactive Job" system. During the execution of a workflow, an interactive job will allow human actors to complete a task as part of the workflow. This can be for quality control (verifying the output of an automated process), correction (adjusting the output of an automated process), or task completion (tasks for which humans perform better than machines).

The Rodan server is accessed and controlled via a REST API, making it possible to create a wide variety of user interfaces and scripts to interact with and control workflow creation and execution. The Rodan Client is a general-purpose user interface, but other dedicated user interfaces can be created to interact with a particular part of the workflow process; for example, crowdsourcing interfaces may be built to distribute interactive job processes to a large audience of human actors.

Rodan automatically parallelizes resource processing over a number of available worker systems. This provides the ability to process large numbers of files given a suitably large cluster of available computer systems. Once a job has finished executing, the output of the process is stored centrally, allowing the output of any job to be the input of any other job in a different workflow.

To find out more about Rodan, please see the full documentation on our GitHub wiki.