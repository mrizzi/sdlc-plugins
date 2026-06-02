## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` column, entity definition updates, advisory service/endpoint query updates, ingestion pipeline updates, and integration test updates. All changes must land together to maintain database-code consistency.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes: migration, entity updates, service/endpoint updates, ingestion pipeline updates, test updates
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch (`cargo test`)
- [ ] Migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create database migration for advisory_status_enum
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update advisory ingestion pipeline
- Depends on: Task 6 — Update advisory integration tests
