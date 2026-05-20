# Task 8 — Merge feature branch TC-9003 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9003` into `main`. The PR description should summarize all changes made across the feature's tasks: the new SBOM comparison diff models, service logic, and endpoint in the backend, plus the API types, comparison page, and list page selection in the frontend.

## Acceptance Criteria
- [ ] A PR from `TC-9003` to `main` is open and ready for review for trustify-backend
- [ ] A PR from `TC-9003` to `main` is open and ready for review for trustify-ui
- [ ] PR descriptions summarize all changes from the feature

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All CI checks pass on the merge PR

## Dependencies
- Depends on: Task 2 — Add SBOM comparison diff model structs
- Depends on: Task 3 — Add SBOM comparison service logic
- Depends on: Task 4 — Add SBOM comparison endpoint
- Depends on: Task 5 — Add API types and client function for SBOM comparison
- Depends on: Task 6 — Create SBOM comparison page with diff sections
- Depends on: Task 7 — Add SBOM selection and "Compare selected" to list page
