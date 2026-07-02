## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks, covering both trustify-backend (comparison model, service, and endpoint) and trustify-ui (API client, comparison page, and list page selection) changes.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all implementation changes from Tasks 2-6

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model types and diff service logic
- Depends on: Task 3 — Add SBOM comparison REST endpoint and integration tests
- Depends on: Task 4 — Add comparison API types, REST client function, and React Query hook
- Depends on: Task 5 — Add SBOM comparison page with diff section components
- Depends on: Task 6 — Update SBOM list page with comparison selection and navigation
