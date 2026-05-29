## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new backend SBOM comparison endpoint with diff computation service, new frontend comparison page with SBOM selectors and six collapsible diff sections, route registration with shareable URL support, and supporting API types, hooks, and tests.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison response model types
- Depends on: Task 3 — Add SBOM comparison service with diff logic
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint and integration tests
- Depends on: Task 5 — Add SBOM comparison API types and client function
- Depends on: Task 6 — Add useSbomComparison React Query hook
- Depends on: Task 7 — Add SBOM comparison page UI with diff sections
- Depends on: Task 8 — Add comparison route and E2E tests

[sdlc-workflow] Description digest: sha256:684da1a9d53e2425b277c9b23b5dec4b12931a6cc6e2c5c54774e96f1b790bc7
