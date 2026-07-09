## Repository
trustify-backend

## Target Branch
main

## Bookend Type
merge-branch

## Description
Create a PR to merge feature branch `TC-9005` into `main`. The PR description should summarize all changes made across the feature's tasks:

- Database migration: replaced `advisory_status` lookup table with `advisory_status_enum` PostgreSQL enum column on the `advisory` table, with atomic backfill and rollback support
- Entity updates: defined `AdvisoryStatusEnum` with SeaORM `DeriveActiveEnum`, updated `advisory` entity, removed `advisory_status` entity
- Service and endpoint updates: eliminated `advisory_status` join from all advisory queries, using `advisory.status` enum column directly for filtering and selection
- Ingestion pipeline: writes enum values directly to `advisory.status` instead of inserting into lookup table
- Integration tests: updated test data seeding and assertions for enum-based status column
- Documentation: updated internal architecture docs to reflect the schema change

## Acceptance Criteria
- [ ] A PR from `TC-9005` to `main` is open and ready for review
- [ ] All CI checks pass on the PR
- [ ] PR description summarizes all feature changes across all tasks

## Test Requirements
- [ ] Verify all intermediate task PRs have been merged into the feature branch before creating the merge PR
- [ ] Verify no merge conflicts exist with current `main`
- [ ] Verify all tests pass on the feature branch (`cargo test`)

## Dependencies
- Depends on: Task 2 -- Create database migration for advisory status enum
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
- Depends on: Task 4 -- Update advisory service and endpoints to use enum status column
- Depends on: Task 5 -- Update advisory ingestion pipeline to write enum status directly
- Depends on: Task 6 -- Update integration tests for advisory status enum
- Depends on: Task 7 -- Update architecture documentation for schema change
