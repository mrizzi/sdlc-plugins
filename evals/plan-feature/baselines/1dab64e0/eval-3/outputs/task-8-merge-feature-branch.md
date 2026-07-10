## Repository
trustify-ui

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison backend endpoint (`GET /api/v2/sbom/compare`), comparison page UI with PatternFly diff sections, API types and React Query hook, SBOM list page compare action, and documentation updates.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison models and diff service
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests
- Depends on: Task 4 — Add SBOM comparison API types, client function, and hook
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add compare action to SBOM list page
- Depends on: Task 7 — Document SBOM comparison endpoint and UI workflow
