## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the feature branch `TC-9003` into `main` in both `trustify-backend` and `trustify-ui` repositories after all intermediate tasks have been completed and their PRs merged to the feature branch. This finalizes the SBOM comparison view feature.

## Dependencies
- Depends on: Task 6 — Frontend tests and mocks (all intermediate tasks must be complete)

## Acceptance Criteria
- [ ] Feature branch `TC-9003` is merged to `main` in `trustify-backend`
- [ ] Feature branch `TC-9003` is merged to `main` in `trustify-ui`
- [ ] All CI checks pass on the merge commits
- [ ] Feature branch `TC-9003` is deleted in both repositories after merge
