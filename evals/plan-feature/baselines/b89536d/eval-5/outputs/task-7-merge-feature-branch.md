## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: the advisory_status_enum migration, entity definition updates, service/endpoint query simplification, ingestion pipeline changes, and integration test updates. This ensures all changes land atomically on main, preventing any partial state where the migration exists without the code changes or vice versa.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-6

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-6) have been merged into the feature branch before creating the merge PR
- [ ] All CI checks pass on the feature branch before the merge PR is created

## Dependencies
- Depends on: Task 2 — Create advisory_status_enum migration
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Update integration tests
