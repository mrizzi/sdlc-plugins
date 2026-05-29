## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: the database migration replacing the `advisory_status` lookup table with a PostgreSQL enum column, the updated SeaORM entity definitions, and the updated service layer, endpoints, and ingestion pipeline. This ensures all interdependent changes land on `main` atomically.

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes: migration, entity updates, service/endpoint/ingestion updates
- [ ] All CI checks pass on the PR

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify the full workspace builds and all tests pass on the feature branch (`cargo build --workspace && cargo test --workspace`)

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service, endpoints, and ingestion pipeline


[sdlc-workflow] Description digest: sha256:7e365551e2e8cc91b8a078561ebc46f0f6deb242ce7209c816fbdcbb9bff5261
