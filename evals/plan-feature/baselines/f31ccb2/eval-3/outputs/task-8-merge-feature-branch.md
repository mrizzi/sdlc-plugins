# Task 8 — Merge feature branch TC-9003 to main

**Summary:** Merge feature branch TC-9003 to main

**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: new SBOM comparison model structs, comparison diffing service logic, GET /api/v2/sbom/compare endpoint, integration tests in the backend, and the frontend comparison page with API layer, diff section components, and unit tests.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison response model structs
- Depends on: Task 3 — Add SBOM comparison diffing service logic
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 5 — Add integration tests for SBOM comparison endpoint
- Depends on: Task 6 — Add frontend API types, client function, and React Query hook for SBOM comparison
- Depends on: Task 7 — Create SBOM comparison page with header toolbar and diff sections
