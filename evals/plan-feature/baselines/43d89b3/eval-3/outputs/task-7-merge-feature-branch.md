## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: backend SBOM comparison endpoint with structured diff computation, and frontend comparison page with PatternFly UI components, URL-shareable state, and SBOM list page integration.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model and diff service
- Depends on: Task 3 — Add comparison REST endpoint and integration tests
- Depends on: Task 4 — Add SBOM comparison API client and React Query hook
- Depends on: Task 5 — Implement SBOM comparison page with PatternFly components
- Depends on: Task 6 — Add comparison route and URL-shareable state
