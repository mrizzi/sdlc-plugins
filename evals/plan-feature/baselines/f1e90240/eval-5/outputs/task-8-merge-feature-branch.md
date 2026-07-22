# Task 8 -- Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column, SeaORM entity updates, advisory service and endpoint query simplification, ingestion pipeline update, integration test updates, and architecture documentation updates.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-7

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-7) have been merged into the feature branch before creating the merge PR
- [ ] Full test suite passes on the feature branch

## Dependencies
- Depends on: Task 2 -- Create migration: add advisory_status_enum type, backfill status column, drop lookup table
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use enum status column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 -- Update advisory integration tests for enum status
- Depends on: Task 7 -- Update internal architecture documentation
