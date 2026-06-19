## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge the feature branch TC-9005 to main. This aggregates all intermediate changes -- the database migration, entity definition updates, service and endpoint updates, ingestion pipeline updates, and integration test updates -- into a single merge PR, ensuring the breaking schema change and its corresponding code updates land atomically on main.

## Acceptance Criteria
- [ ] PR from `TC-9005` to `main` is created
- [ ] All intermediate task PRs have been merged into the feature branch
- [ ] CI passes on the merge PR
- [ ] No merge conflicts with `main`

## Test Requirements
- [ ] All integration tests pass on the feature branch before merge
- [ ] CI pipeline passes on the merge PR

## Dependencies
- Depends on: Task 2 -- Database migration (enum column)
- Depends on: Task 3 -- Update entity definitions
- Depends on: Task 4 -- Update advisory service and endpoints
- Depends on: Task 5 -- Update ingestion pipeline
- Depends on: Task 6 -- Update integration tests
