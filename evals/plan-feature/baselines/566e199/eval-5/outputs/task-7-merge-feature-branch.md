# Task 7 -- Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: atomic database migration replacing `advisory_status` lookup table with `advisory_status_enum` column, updated SeaORM entities, updated advisory service/endpoints, updated ingestion pipeline, and updated integration tests. All intermediate task PRs must be merged into the feature branch before creating this merge PR.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from the feature
- [ ] All CI checks pass on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch (`cargo test`)
- [ ] Migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 -- Create atomic migration to replace advisory_status table with enum column
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 -- Update advisory integration tests for enum status column
