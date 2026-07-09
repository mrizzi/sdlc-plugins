## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9006` into `main`. The PR description should summarize all changes made across the feature's tasks: new remediation aggregation endpoints in the backend (GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product), and the remediation dashboard page with summary cards, progress chart, and filterable vulnerability table in the frontend.

## Acceptance Criteria
- [ ] A PR from `TC-9006` to `main` is open and ready for review

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 -- Add remediation module with summary aggregation service and endpoint
- Depends on: Task 3 -- Add per-product remediation breakdown endpoint
- Depends on: Task 4 -- Add integration tests for remediation endpoints
- Depends on: Task 5 -- Add remediation API types, client functions, and React Query hooks
- Depends on: Task 6 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard
- Depends on: Task 8 -- Register /remediation route and add navigation entry
- Depends on: Task 9 -- Document remediation dashboard and API endpoints
