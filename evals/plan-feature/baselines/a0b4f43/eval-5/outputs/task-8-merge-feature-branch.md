## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from lookup table to enum column, entity definition updates, service layer query simplification, endpoint updates, ingestion pipeline changes, and integration test updates. This ensures all interdependent changes land on `main` atomically.

## Acceptance Criteria
- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from the feature's tasks
- [ ] All CI checks pass on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch: `cargo test`
- [ ] Verify the migration runs successfully: `cargo run --bin migration -- up`

## Dependencies
- Depends on: Task 2 — Create migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and models
- Depends on: Task 5 — Update advisory endpoints
- Depends on: Task 6 — Update ingestion pipeline
- Depends on: Task 7 — Update integration tests