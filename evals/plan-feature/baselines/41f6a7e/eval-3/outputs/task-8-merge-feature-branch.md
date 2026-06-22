# Task 8 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the new SBOM comparison diff model and service (Task 2), the comparison REST endpoint (Task 3), the frontend API layer and hooks (Task 4), the comparison page UI (Task 5), the SBOM list page compare action (Task 6), and the E2E tests (Task 7).

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review
- [ ] PR description summarizes all changes from Tasks 2-7

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All CI checks pass on the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model and service
- Depends on: Task 3 — Add SBOM comparison REST endpoint
- Depends on: Task 4 — Add frontend API types, client function, and React Query hook for SBOM comparison
- Depends on: Task 5 — Add SBOM comparison page with diff sections
- Depends on: Task 6 — Add "Compare selected" action to SBOM list page
- Depends on: Task 7 — Add E2E test for SBOM comparison workflow
