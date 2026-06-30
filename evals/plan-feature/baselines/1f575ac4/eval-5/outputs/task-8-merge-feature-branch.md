# Task 8 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: the database migration from `advisory_status` lookup table to `advisory_status_enum` column, the entity layer updates, the service and endpoint query simplification, the ingestion pipeline update, and the integration test updates. This PR represents the atomic delivery of the entire "Drop status table and migrate to enum column" feature.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2 through 7
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2–7) have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify the migration runs successfully against a clean database

## Dependencies
- Depends on: Task 2 — Create database migration: advisory_status enum column and drop lookup table
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service layer and models to use enum status
- Depends on: Task 5 — Update advisory endpoints to filter by enum status column
- Depends on: Task 6 — Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 7 — Update advisory integration tests for enum-based status
