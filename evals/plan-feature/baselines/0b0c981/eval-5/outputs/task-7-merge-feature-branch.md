## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from lookup table to enum column, entity definition updates, advisory service and endpoint refactoring, ingestion pipeline update, and integration test updates. This PR delivers the complete "Drop status table and migrate to enum column" feature atomically to `main`.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] The PR description summarizes all changes from tasks 2 through 6
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full test suite passes on the feature branch (`cargo test`)

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update advisory ingestion pipeline
- Depends on: Task 6 — Update integration tests

[sdlc-workflow] Description digest: sha256:411555da90b31ab9dfb334eb56b00c571eb33d87dfb6a3b8c061a6c790396535
