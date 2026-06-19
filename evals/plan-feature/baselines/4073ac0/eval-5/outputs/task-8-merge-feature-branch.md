## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Merge feature branch `TC-9005` to `main` after all intermediate tasks are complete. This delivers the full advisory status enum migration atomically — the database migration, entity updates, service layer changes, endpoint updates, ingestion pipeline updates, and integration tests all land together, preventing the inconsistent state that would result from partial delivery.

## Acceptance Criteria
- [ ] All intermediate tasks (Tasks 2-7) are complete and merged to `TC-9005`
- [ ] All tests pass on the `TC-9005` branch
- [ ] Feature branch `TC-9005` is merged to `main` via pull request
- [ ] No merge conflicts with `main`
- [ ] CI pipeline passes on the merge commit

## Test Requirements
- [ ] Full test suite passes on `TC-9005` branch before merge (`cargo test`)
- [ ] Migration up and down succeed on a clean database
- [ ] Advisory list endpoint returns correct status values
- [ ] Advisory ingestion correctly writes enum status values

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service layer and models to use enum column
- Depends on: Task 5 — Update advisory endpoints for enum-based status filtering
- Depends on: Task 6 — Update advisory ingestion pipeline to write enum status
- Depends on: Task 7 — Update advisory integration tests for enum status
