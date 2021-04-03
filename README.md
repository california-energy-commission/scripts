# CEC Scripts

[![GitHub Actions](https://github.com/california-energy-commission/Scripts/actions/workflows/test-deploy.yml/badge.svg)](https://github.com/california-energy-commission/Scripts/actions/workflows/test-deploy.yml)

Test, lint and deploy schema files in all CEC repositories

## How it works

- A regular push happens to a repository A.
- This will trigger a workflow execution in repository A.
- This workflow will perform a request to the dispatches endpoint in repository Scripts with a `dispatch` action type and end its execution.
- Repository Scripts will start a new workflow execution (test, lint and deploy) using the contents of Repository A.
- After finishing this workflow, repository Scripts will send a `response` event type back to the repository A.

![actions-remote-dispatch-sequence-diagram](https://user-images.githubusercontent.com/1832537/113183794-ccf7b680-922a-11eb-9853-55ba5e994254.png)