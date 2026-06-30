# Task 1 — Create feature branch TC-9005 from main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the "Drop status table and migrate to enum column" feature will target this branch. This ensures all changes land atomically — the migration, entity updates, service/endpoint updates, ingestion changes, and test updates must all be present before merging to `main`.

## Acceptance Criteria
- [ ] The feature branch `TC-9005` exists on the remote repository
- [ ] The branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
- None (this is the first task)
