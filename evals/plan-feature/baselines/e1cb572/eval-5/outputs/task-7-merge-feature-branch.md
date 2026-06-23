# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` PostgreSQL enum column, SeaORM entity updates, advisory service and endpoint query simplification, ingestion pipeline update, and integration test updates. This PR delivers the complete "Drop status table and migrate to enum column" feature atomically to `main`.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from Tasks 2-6
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs (Tasks 2-6) have been merged into the feature branch before creating the merge PR
- [ ] Full test suite passes on the feature branch (`cargo test`)
- [ ] Migration applies and reverts cleanly (`cargo run --bin migration -- up` and `down`)

## Dependencies
- Depends on: Task 2 -- Add database migration for advisory status enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use status enum
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum status
- Depends on: Task 6 -- Update advisory integration tests for enum status

`[sdlc-workflow] Description digest: sha256-md:a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2`
