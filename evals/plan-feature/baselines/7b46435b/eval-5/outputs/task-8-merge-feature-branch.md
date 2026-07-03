## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a pull request to merge feature branch TC-9005 into main. This PR aggregates all changes for dropping the advisory_status lookup table and migrating to an advisory_status_enum column: the atomic database migration, updated SeaORM entity definitions, updated advisory service/endpoints, updated ingestion pipeline, updated integration tests, and documentation updates. All changes must land together to maintain database-code consistency.

## Acceptance Criteria
- [ ] PR is created from TC-9005 to main
- [ ] All intermediate task PRs have been merged into TC-9005
- [ ] CI passes on the feature branch
- [ ] PR description summarizes all changes included in the feature branch

## Test Requirements
- [ ] All tests pass on the TC-9005 branch before creating the merge PR
- [ ] Migration runs successfully against the test database
- [ ] Integration tests pass with the new schema

## Dependencies
- Depends on: Task 2 — Database migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Update integration tests
- Depends on: Task 7 — Update documentation
