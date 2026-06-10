## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison endpoint in trustify-backend, comparison page UI with PatternFly components in trustify-ui, SBOM list selection integration, and E2E tests.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-8

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-8) have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison response model types
- Depends on: Task 3 — Add SBOM comparison service logic
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 5 — Add frontend API layer for SBOM comparison
- Depends on: Task 6 — Add SBOM comparison page UI
- Depends on: Task 7 — Add SBOM selection UI to SbomListPage
- Depends on: Task 8 — Add E2E tests for SBOM comparison workflow
