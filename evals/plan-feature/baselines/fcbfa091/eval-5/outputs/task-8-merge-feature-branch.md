# Task 8: Merge feature branch TC-9005 to main

## Bookend Type
merge-branch

## Repository
trustify-backend

## Target Branch
main

## Description
Merge the feature branch `TC-9005` to `main` by creating a pull request that includes all changes from the advisory status enum migration. This PR encompasses the database migration, entity definition updates, service layer changes, ingestion pipeline updates, endpoint modifications, and integration test updates. All changes must land atomically to prevent the database schema and application code from diverging -- merging the migration alone would break queries that still join the dropped table, and merging code changes alone would reference a column that does not yet exist.

## Acceptance Criteria
- [ ] Pull request is created from `TC-9005` to `main`
- [ ] All CI checks pass on the pull request
- [ ] No merge conflicts with `main`
- [ ] PR description summarizes all changes: migration, entities, service, ingestion, endpoints, tests
- [ ] PR is approved and merged

## Test Requirements
- [ ] All integration tests pass on the feature branch before merge
- [ ] CI pipeline completes successfully
- [ ] Post-merge: `cargo test` passes on `main`

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service layer and models
- Depends on: Task 5 -- Update advisory ingestion pipeline
- Depends on: Task 6 -- Update advisory endpoints for enum status
- Depends on: Task 7 -- Update advisory integration tests

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0
