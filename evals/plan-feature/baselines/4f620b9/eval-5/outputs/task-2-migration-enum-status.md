# Task 2 — Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected; (2) add a `status` enum column to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join via `status_id`; (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` lookup table. The migration must be atomic — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- The migration must be wrapped in a transaction to ensure atomicity — use `manager.get_connection()` with explicit transaction handling if SeaORM's migration runner does not provide implicit transactions.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for PostgreSQL-specific `CREATE TYPE` and `DROP TYPE` statements since SeaORM's schema builder does not natively support enum types.
- Backfill strategy: use `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum` or equivalent to populate the enum column before dropping the FK.
- The `down()` migration must reverse all steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop `advisory_status_enum` type.
- Zero downtime consideration: since all changes land on a feature branch and deploy together, the migration and code changes are guaranteed to be in sync at deployment time.
- Per docs/constraints.md §2 (Commit Rules): commits must follow Conventional Commits format with Jira issue ID in footer and `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to listed files; inspect existing migration code before implementing.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the SeaORM migration trait pattern, table creation, and schema operations

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL type is created with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory.status` enum column is added and populated from existing `status_id` join
- [ ] `advisory.status_id` foreign key column is dropped
- [ ] `advisory_status` lookup table is dropped
- [ ] Migration is reversible — `down()` restores the previous schema
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run the migration up and verify the enum type exists: `SELECT typname FROM pg_type WHERE typname = 'advisory_status_enum'`
- [ ] Verify `advisory.status` column exists and contains correct values after backfill
- [ ] Verify `advisory_status` table no longer exists after migration
- [ ] Run the migration down and verify the original schema is restored
- [ ] Test migration against a database with existing advisory data to confirm backfill correctness

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:2b1eba909ca2bde4aa6e0718a09a80bd21e1f74f7df2693dd5f84768fbf7fd3f
