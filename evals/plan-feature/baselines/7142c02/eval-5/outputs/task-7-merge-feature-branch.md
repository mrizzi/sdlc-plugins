## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Jira Metadata
- Priority: High
- Fix Version: RHTPA 2.0.0

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks: database migration from advisory_status lookup table to PostgreSQL enum column, updated SeaORM entity definitions, updated advisory service/endpoints/models, updated ingestion pipeline, and updated integration tests. All intermediate task PRs must be merged into the feature branch before creating this merge PR.

## Acceptance Criteria
- [ ] All intermediate task PRs (Tasks 2-6) have been merged into the `TC-9005` feature branch
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] PR description summarizes all changes across the feature

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] All tests pass on the feature branch with the combined changes
- [ ] Migration runs successfully on a clean database with all code changes present

## Dependencies
- Depends on: Task 2 — Create database migration for advisory status enum
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 — Update advisory service and endpoints to use enum status
- Depends on: Task 5 — Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 6 — Update integration tests for advisory status enum migration

[sdlc-workflow] Description digest: sha256-md:4a3d92986842269ef621812a659ed4fc6b0cfb36e83812a171c0b80fc6d26ca1
