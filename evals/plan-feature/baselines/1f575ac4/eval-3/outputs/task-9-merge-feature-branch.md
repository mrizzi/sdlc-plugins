## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: backend SBOM comparison endpoint with structured diff computation, frontend comparison page with SBOM selectors and diff sections, SBOM list page compare action, and E2E tests.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged into the feature branch `TC-9003`
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from the SBOM comparison view feature

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify CI passes on the merge PR

## Dependencies
- Depends on: Task 2 — Backend comparison response model
- Depends on: Task 3 — Backend comparison service logic
- Depends on: Task 4 — Backend comparison endpoint
- Depends on: Task 5 — Frontend API layer
- Depends on: Task 6 — Frontend comparison page
- Depends on: Task 7 — SBOM list page compare action
- Depends on: Task 8 — E2E test
