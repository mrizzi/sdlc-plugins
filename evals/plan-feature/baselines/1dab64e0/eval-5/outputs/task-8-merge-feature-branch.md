## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from the `advisory_status` lookup table to a PostgreSQL enum column, SeaORM entity updates, advisory service and endpoint query simplification, ingestion pipeline update, and integration test updates. All intermediate task PRs must be merged into the feature branch before creating this merge PR.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from the feature's implementation tasks
- [ ] All intermediate task PRs have been merged into the `TC-9005` feature branch
- [ ] All CI checks pass on the merge PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the merge PR includes all commits from the feature branch
- [ ] Verify CI passes on the merge PR (all tests, compilation, linting)

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum conversion
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline for direct enum status writes
- Depends on: Task 6 — Update advisory integration tests for status enum
- Depends on: Task 7 — Update internal architecture documentation
