## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create feature branch `TC-9005` from `main` for the advisory status table to enum column migration. This feature requires feature-branch workflow because the database migration and code changes are mutually dependent — the migration drops the `advisory_status` table and adds a `status` enum column, while the code changes reference the new column and remove the old join. Merging either side independently would break all advisory queries.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists, branched from the current tip of `main`
- [ ] Branch is pushed to the remote repository

## Test Requirements
- [ ] Branch exists locally and on remote
- [ ] Branch point matches current `main` HEAD

## Dependencies
None
