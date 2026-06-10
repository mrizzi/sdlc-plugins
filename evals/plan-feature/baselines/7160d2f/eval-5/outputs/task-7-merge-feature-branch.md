## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: creation of the `advisory_status_enum` PostgreSQL type, migration from the `advisory_status` lookup table to a direct enum column on the `advisory` table, updated entity definitions, service layer and endpoint changes to eliminate the join, ingestion pipeline updates, and integration test updates.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-6
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-6) have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch before opening the PR

## Dependencies
- Depends on: Task 2 — Create advisory_status_enum migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update advisory ingestion pipeline
- Depends on: Task 6 — Update advisory integration tests
