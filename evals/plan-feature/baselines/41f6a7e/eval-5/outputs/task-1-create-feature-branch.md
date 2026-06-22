# Task 1 — Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This ensures that the database migration, entity changes, service updates, ingestion changes, and test updates all land together before merging to `main`.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists locally and is pushed to the remote
- [ ] The branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
- None — this is the first task
