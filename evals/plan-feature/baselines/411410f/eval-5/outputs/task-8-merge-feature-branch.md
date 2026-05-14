# Task 8 -- Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a pull request to merge the feature branch `TC-9005` into `main`. This PR aggregates all changes from the advisory status enum migration: the database migration, entity definition updates, service/model layer changes, endpoint updates, ingestion pipeline changes, and integration test updates. All changes land atomically on main, ensuring the migration and code changes are never out of sync.

## Acceptance Criteria
- [ ] PR is created from `TC-9005` to `main`
- [ ] All intermediate task PRs have been merged to the feature branch
- [ ] CI passes on the feature branch
- [ ] No remaining references to `advisory_status` lookup table in any modified file
- [ ] Migration, entity, service, endpoint, ingestion, and test changes are all present in the PR

## Test Requirements
- [ ] Full test suite passes on the feature branch (`cargo test`)
- [ ] Migration runs successfully against a clean database
- [ ] Advisory list and get endpoints return correct responses
- [ ] Advisory ingestion pipeline writes enum values correctly

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and model layers
- Depends on: Task 5 -- Update advisory endpoints for enum status
- Depends on: Task 6 -- Update advisory ingestion pipeline for enum status
- Depends on: Task 7 -- Update integration tests for advisory status enum
