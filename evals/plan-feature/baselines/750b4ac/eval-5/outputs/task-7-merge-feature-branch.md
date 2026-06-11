# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from advisory_status lookup table to PostgreSQL enum column, SeaORM entity updates, advisory service/model query changes, ingestion pipeline updates, endpoint modifications, and integration test updates. This PR represents the atomic delivery of the complete advisory status enum migration.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes from tasks 2-6
- [ ] All CI checks pass on the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs (tasks 2-6) have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch (`cargo test`)

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service layer and models to use status enum
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory endpoints and integration tests

[sdlc-workflow] Description digest: sha256-md:afcdad11164ad34b3a2c0a8fc1b0d1e150dec8c1f5716637c7a3d4095a61a22f
