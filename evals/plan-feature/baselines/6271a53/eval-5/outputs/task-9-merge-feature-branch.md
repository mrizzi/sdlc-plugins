## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: migration from advisory_status lookup table to PostgreSQL enum column, entity definition updates, service layer changes, endpoint updates, ingestion pipeline changes, and integration test updates. This is the final step that delivers all changes atomically to main.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes across the feature
- [ ] All CI checks pass on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify the migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 -- Create migration for advisory_status_enum and drop lookup table
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory model structs for enum status
- Depends on: Task 5 -- Update AdvisoryService to use enum status column
- Depends on: Task 6 -- Update advisory endpoints for enum status
- Depends on: Task 7 -- Update advisory ingestion pipeline for enum status
- Depends on: Task 8 -- Update advisory integration tests for enum status
