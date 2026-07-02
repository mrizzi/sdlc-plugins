## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the `TC-9003` feature branch into `main` in the trustify-backend repository after all backend comparison tasks are complete. Create a pull request summarizing the SBOM comparison endpoint changes for review.

## Acceptance Criteria
- [ ] Pull request from `TC-9003` to `main` is created in trustify-backend
- [ ] All CI checks pass on the PR
- [ ] PR is merged after approval

## Test Requirements
- [ ] All existing tests continue to pass after merge
- [ ] SBOM comparison integration tests pass in CI

## Dependencies
- Depends on: Task 3 -- Add SBOM comparison model types and diff service
- Depends on: Task 4 -- Add SBOM comparison endpoint and integration tests

## Additional Fields
- priority: Critical
- fixVersions: RHTPA 1.5.0
- labels: ai-generated-jira
