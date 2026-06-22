# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration replacing the `advisory_status` lookup table with an `advisory_status_enum` column, entity definition updates, service/endpoint query simplification, ingestion pipeline updates, and integration test updates. This delivers the complete advisory status enum migration as an atomic unit.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes: migration, entity updates, service/endpoint updates, ingestion updates, and test updates
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify all tests pass on the feature branch: `cargo test`
- [ ] Verify the migration runs cleanly: `cargo run --bin migration -- up`

## Dependencies
- Depends on: Task 2 — Create migration to replace advisory_status table with enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum status column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 6 — Update advisory integration tests for enum status column
