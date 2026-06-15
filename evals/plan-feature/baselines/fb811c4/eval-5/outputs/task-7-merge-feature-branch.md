## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch TC-9005 into main. The PR description should summarize all changes made across the feature's tasks: the atomic database migration from advisory_status lookup table to PostgreSQL enum column, SeaORM entity updates, advisory service and endpoint changes, ingestion pipeline updates, and integration test additions.

## Acceptance Criteria
- [ ] A PR from TC-9005 to main is open and ready for review
- [ ] PR description summarizes all changes from the feature branch

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All CI checks pass on the feature branch

## Dependencies
- Depends on: Task 2 — Database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions
- Depends on: Task 4 — Update advisory service and endpoints
- Depends on: Task 5 — Update ingestion pipeline
- Depends on: Task 6 — Integration tests for advisory status enum

[sdlc-workflow] Description digest: sha256-md:2d17ab6e5d02414a1b7ae4ef0eebda8d463279d842dd5af8a85725c6ee9cb48d
