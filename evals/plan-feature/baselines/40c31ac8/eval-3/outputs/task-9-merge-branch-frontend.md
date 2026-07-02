## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the `TC-9003` feature branch into `main` in the trustify-ui repository after all frontend comparison tasks are complete. Create a pull request summarizing the SBOM comparison UI changes for review.

## Acceptance Criteria
- [ ] Pull request from `TC-9003` to `main` is created in trustify-ui
- [ ] All CI checks pass on the PR
- [ ] PR is merged after approval

## Test Requirements
- [ ] All existing tests continue to pass after merge
- [ ] SBOM comparison page tests pass in CI

## Dependencies
- Depends on: Task 5 -- Add API types, client function, and React Query hook for SBOM comparison
- Depends on: Task 6 -- Implement SBOM comparison page UI
- Depends on: Task 7 -- Add comparison route and compare action from SBOM list

## Additional Fields
- priority: Critical
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
