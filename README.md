# CEC Scripts

[![Remote Dispatch Action Responder](https://github.com/california-energy-commission/Scripts/actions/workflows/test-deploy.yml/badge.svg)](https://github.com/california-energy-commission/Scripts/actions/workflows/test-deploy.yml)

Test, lint and deploy schema files in all CEC repositories

## How it works

A regular push happens to any repository A. This will trigger a workflow execution in repository A, this workflow will perform a request to the dispatches endpoint in repository Scripts with a `dispatch` action type and end its execution.

Repository Scripts will start a new workflow execution (test, lint and deploy) using the contents of Repository A.

![actions-remote-dispatch-sequence-diagram](https://user-images.githubusercontent.com/1832537/113180905-a3895b80-9227-11eb-9bb2-1700d8fd3fed.png)