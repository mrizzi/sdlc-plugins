## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the new SBOM comparison backend endpoint (`GET /api/v2/sbom/compare`), the comparison service and model structs, the frontend comparison page with diff sections, the API types/hooks, and the SBOM list page selection support.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from tasks 2 through 7

## Test Requirements
- [ ] Verify all intermediate task PRs (tasks 2-7) have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison model structs
- Depends on: Task 3 — Implement SBOM comparison service
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint
- Depends on: Task 5 — Add comparison API types, client function, and React Query hook
- Depends on: Task 6 — Build SBOM comparison page UI
- Depends on: Task 7 — Add SBOM list page selection and Compare action
