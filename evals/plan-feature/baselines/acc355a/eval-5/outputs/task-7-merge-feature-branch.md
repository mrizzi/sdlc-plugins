# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration replacing the `advisory_status` lookup table with an `advisory_status_enum` PostgreSQL enum column on the `advisory` table
- Updated SeaORM entity definitions removing the `advisory_status` entity and adding `AdvisoryStatusEnum` to the advisory entity
- Updated advisory service layer and endpoints to query using the `status` enum column directly (no join)
- Updated advisory ingestion pipeline to write enum values directly
- Updated integration tests for the new schema

This migration eliminates unnecessary join overhead on every advisory query, reduces advisory list endpoint p95 latency by approximately 40ms, and simplifies the schema by removing the `advisory_status` lookup table.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from the feature's intermediate tasks
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify all tests pass on the feature branch before creating the merge PR

## Dependencies
- Depends on: Task 2 — Create database migration to replace advisory_status table with enum column
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for status enum column
