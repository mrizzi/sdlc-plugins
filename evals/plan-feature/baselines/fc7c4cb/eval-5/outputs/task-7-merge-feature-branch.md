# Task 7 — Merge feature branch TC-9005 to main

## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from `advisory_status` lookup table to `advisory_status_enum` column, SeaORM entity updates, advisory service and endpoint query changes, ingestion pipeline updates, and integration test updates.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] All CI checks pass on the merge PR
- [ ] The PR description summarizes the complete set of changes from all intermediate tasks

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)
- [ ] Verify the migration runs successfully against a clean database (`cargo run --bin migration -- up`)

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use status enum column
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum values directly
- Depends on: Task 6 — Update advisory integration tests for enum-based status

[sdlc-workflow] Description digest: sha256:ba4a66673f8f86332c76cf1dc777adae5d24cd6081727d81abc908b960bb8a3e
