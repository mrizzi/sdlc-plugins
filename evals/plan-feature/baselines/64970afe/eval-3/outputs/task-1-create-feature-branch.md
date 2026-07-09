## Repository
trustify-ui

## Target Branch
main

## Bookend Type
create-branch

## Description
Create and push the feature branch `TC-9003` from the latest `main`. All subsequent implementation tasks for the SBOM comparison view feature will target this branch. Both trustify-backend and trustify-ui repositories require this feature branch since the feature spans both repositories.

## Acceptance Criteria
- [ ] The feature branch `TC-9003` exists in the trustify-ui remote
- [ ] The feature branch `TC-9003` exists in the trustify-backend remote
- [ ] Both branches are created from the latest `main`

## Test Requirements
- [ ] Verify the branch `TC-9003` exists on the remote after push (`git ls-remote --heads origin TC-9003`)
- [ ] Verify the branch points to the same commit as `main` at creation time

## Dependencies
- None (first task)
