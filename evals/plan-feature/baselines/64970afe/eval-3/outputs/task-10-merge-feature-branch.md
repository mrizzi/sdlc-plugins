## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks for the SBOM comparison view, covering both the trustify-backend (comparison model, service, endpoint, integration tests) and trustify-ui (API types, comparison page, route registration, list page integration, tests) repositories.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged into the feature branch `TC-9003`
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-ui
- [ ] A PR from `TC-9003` to `main` is open and ready for review in trustify-backend
- [ ] PR descriptions summarize all changes from the SBOM comparison feature

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify CI passes on the feature branch before creating the merge PR
- [ ] Verify no merge conflicts with `main`

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model types and diff service
- Depends on: Task 3 — Add SBOM comparison REST endpoint
- Depends on: Task 4 — Add integration tests for SBOM comparison endpoint
- Depends on: Task 5 — Add TypeScript types, API client function, and React Query hook for SBOM comparison
- Depends on: Task 6 — Implement SBOM comparison page with diff sections
- Depends on: Task 7 — Add route registration and SBOM list page compare trigger
- Depends on: Task 8 — Add unit and E2E tests for SBOM comparison page
- Depends on: Task 9 — Document SBOM comparison endpoint and UI workflow
