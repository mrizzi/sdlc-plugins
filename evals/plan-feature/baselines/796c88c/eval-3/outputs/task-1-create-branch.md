## Repository
trustify-backend

## Target Branch
main

## Bookend Type
create-branch

## Description
Create the shared feature branch `TC-9003` in both `trustify-backend` and `trustify-ui` repositories. This branch will be the integration point for all SBOM comparison view work across both repos. Since this is a tightly coupled multi-repo feature (the frontend depends on the new backend endpoint), a shared feature branch ensures both sides can be developed and tested in coordination before merging to main.

## Files to Modify
- None

## Files to Create
- None

## Implementation Notes
Create the branch `TC-9003` from `main` in both repositories:
- `trustify-backend`: `git checkout -b TC-9003 main`
- `trustify-ui`: `git checkout -b TC-9003 main`

No code changes in this task. This is a coordination task to establish the feature branch in both repositories.

## Acceptance Criteria
- [ ] Branch `TC-9003` exists in `trustify-backend` repository, based on latest `main`
- [ ] Branch `TC-9003` exists in `trustify-ui` repository, based on latest `main`
- [ ] Both branches are pushed to their respective remotes

## Dependencies
- None — this is the first task
