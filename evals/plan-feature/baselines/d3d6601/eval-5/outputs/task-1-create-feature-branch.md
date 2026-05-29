## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9005` from the latest `main`. All subsequent implementation tasks for the advisory status enum migration will target this branch. This ensures that the migration, entity updates, and service/ingestion changes all land together atomically before being merged to main.

## Acceptance Criteria
- [ ] Feature branch `TC-9005` exists and is pushed to the remote
- [ ] Branch is created from the latest `main` commit

## Test Requirements
- [ ] Verify the branch `TC-9005` exists on the remote after push (`git ls-remote --heads origin TC-9005`)

## Dependencies
None


[sdlc-workflow] Description digest: sha256:639e29bd757b4576d19610c3bd875e9bc54536a44c42ddd4e80d457d90ab4c29
