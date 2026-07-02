## Summary
Create feature branch TC-9005 from main

## Bookend Type
create-branch

## Repository
trustify-backend

## Target Branch
main

## Description
Create a feature branch `TC-9005` from `main` to isolate all changes for the advisory status enum migration. This feature requires atomic delivery because the database migration, entity updates, service layer changes, and ingestion pipeline changes are interdependent -- merging the migration without the code changes would break all advisory queries (they still join the now-dropped table), and merging the code changes without the migration would reference a column that does not exist.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` is created from the latest `main`
- [ ] Branch is pushed to the remote repository

## Test Requirements
- [ ] Branch exists on the remote and is based on the current `main` HEAD

## Dependencies
- None (this is the first task)

## Additional Fields
- priority: High
- fixVersions: RHTPA 2.0.0
- labels: ai-generated-jira
