## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Jira Metadata
- Priority: High
- Fix Version: RHTPA 2.0.0

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This feature requires feature-branch mode because the database migration and code changes are tightly coupled — merging the migration without the code changes would break all advisory queries, and merging the code changes without the migration would reference a column that does not exist.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists and is pushed to the remote
- [ ] Branch is created from the latest `main`

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push using `git ls-remote --heads origin TC-9005`

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:cbf5df3f0677741d21ba76e786e4e1af4be0df627cf7f0258860169f03b772aa
