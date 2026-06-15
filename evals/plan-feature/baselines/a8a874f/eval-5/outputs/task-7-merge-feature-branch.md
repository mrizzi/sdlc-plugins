# Task 7: Merge feature branch TC-9005 to main

## Repository

trustify-backend

## Target Branch

main

## Bookend Type

merge-branch

## Description

Create a PR to merge feature branch TC-9005 into main. This PR brings together all the changes for the advisory status table-to-enum migration: the database migration, entity updates, service layer changes, ingestion pipeline updates, and endpoint/test updates. All changes must land atomically to prevent schema-code mismatches.

## Acceptance Criteria

- A PR from TC-9005 to main is open and ready for review
- All intermediate task PRs have been merged into the feature branch
- CI passes on the feature branch with all changes integrated

## Test Requirements

- Verify all intermediate task PRs have been merged into the feature branch
- Verify the feature branch builds and all tests pass with the complete set of changes

## Dependencies

- Task 2: Create PostgreSQL enum type and migration to add status column
- Task 3: Update SeaORM entity definitions for advisory status enum
- Task 4: Update advisory service and model to use enum status
- Task 5: Update advisory ingestion pipeline to write enum values directly
- Task 6: Update advisory endpoints and integration tests

[Description digest: sha256-md:a9e7d3c4b8f50e2c67lc4a0d3b9e8f756c2d4e0a1b3c6d7e8f9a0b1c2d3e4f56 would be posted as a comment]
