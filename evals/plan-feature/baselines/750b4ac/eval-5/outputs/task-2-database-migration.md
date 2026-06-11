# Task 2 — Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: if any step fails, the entire migration rolls back. The migration performs the following steps in order: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `status_id` foreign key join to `advisory_status`; (4) drop the `status_id` foreign key constraint and column from `advisory`; (5) drop the `advisory_status` table.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and registration.
- The migration must be wrapped in a transaction to ensure atomicity — if the backfill or any DDL step fails, all changes roll back.
- Use `extension::postgres::Type::create()` from SeaORM to define the PostgreSQL enum type.
- For the backfill step, use a raw SQL `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)` or equivalent SeaORM expression to populate the enum column from the existing join.
- After backfilling, set the `status` column to `NOT NULL` to enforce data integrity.
- The `down()` method must reverse all steps: recreate `advisory_status` table, add `status_id` column back, backfill from enum, drop enum column, drop enum type.
- Per docs/constraints.md section 2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern showing SeaORM migration structure, table creation, and column definitions

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` column from existing `status_id` join
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible — `down()` method restores the original schema
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Migration runs successfully against a test database with existing advisory data
- [ ] Migration `down()` restores the original schema (advisory_status table, status_id FK)
- [ ] Backfill correctly maps all existing status_id values to enum values
- [ ] Migration fails cleanly if advisory_status table contains unexpected values

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `sea-orm-cli migrate up` — migration applies successfully
- `sea-orm-cli migrate down` — migration rolls back successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:daeccd86d7d176a2f24d7ee97fe43a76d010f4bd90d84e20a7785fbd8e27407d
