## Summary
Merge feature branch TC-9005 to main

## Bookend Type
merge-branch

## Repository
trustify-backend

## Target Branch
main

## Description
Merge the feature branch `TC-9005` back to `main` after all intermediate tasks are complete. This delivers the full advisory status enum migration atomically: the database migration, entity updates, service layer changes, ingestion pipeline updates, endpoint modifications, and integration test updates all land together. This ensures the codebase on `main` never enters an inconsistent state where the migration has run but the code still references the dropped lookup table, or vice versa.

## Acceptance Criteria
- [ ] All intermediate tasks (Tasks 2-6) are complete and merged to `TC-9005`
- [ ] All tests pass on the `TC-9005` branch
- [ ] Feature branch `TC-9005` is merged to `main` via pull request
- [ ] No merge conflicts with `main`
- [ ] `main` branch CI passes after merge

## Test Requirements
- [ ] Full test suite passes on `TC-9005` branch before merge
- [ ] Full test suite passes on `main` after merge

## Dependencies
- Depends on: Task 2 -- Create database migration to replace advisory_status table with enum column
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and model layer to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 -- Update advisory endpoints and integration tests for status enum

## Additional Fields
- priority: High
- fixVersions: RHTPA 2.0.0
- labels: ai-generated-jira
