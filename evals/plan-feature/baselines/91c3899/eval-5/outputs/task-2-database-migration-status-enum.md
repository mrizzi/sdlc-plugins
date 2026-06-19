# Task 2 — Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that performs the full schema transition from the `advisory_status` lookup table to a PostgreSQL enum column on the `advisory` table. The migration must be atomic — if any step fails, the entire migration rolls back. The migration steps are:

1. Create PostgreSQL enum type `advisory_status_enum` with values (`New`, `Analyzing`, `Fixed`, `Rejected`)
2. Add `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill `status` column from the existing `status_id` foreign key join with `advisory_status`
4. Set `status` column to NOT NULL after backfill
5. Drop the `status_id` foreign key constraint and column from `advisory`
6. Drop the `advisory_status` table

The migration must also implement a reversible `down()` method that recreates the lookup table and restores the foreign key relationship.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing the enum transition

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions
- The migration must run within a single transaction to ensure atomicity. If SeaORM does not wrap migrations in a transaction by default, explicitly use `manager.get_connection().begin()` or equivalent
- Use raw SQL for the enum type creation (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`) since SeaORM does not have native enum type creation support
- Backfill the `status` column using an `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)` pattern
- The `down()` method must reverse all steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop enum column, drop enum type
- Zero-downtime requirement: the migration must be safe to run while the application is serving traffic. Since all steps are in a single transaction, this is inherently safe — concurrent reads will see the old schema until the transaction commits
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in the footer and follow Conventional Commits format
- Per docs/constraints.md §3 (PR Rules): PR branch must be named after the Jira issue ID and target branch TC-9005

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration demonstrating the project's SeaORM migration pattern, table creation, and index setup

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` from the existing `status_id` join
- [ ] Migration drops `status_id` column and foreign key constraint
- [ ] Migration drops `advisory_status` table
- [ ] Migration `down()` method reverses all changes
- [ ] Migration is atomic: partial failure rolls back all changes

## Test Requirements
- [ ] Migration runs successfully against a clean database (up)
- [ ] Migration rollback runs successfully (down)
- [ ] After migration, `advisory` table has `status` column of type `advisory_status_enum`
- [ ] After migration, `advisory_status` table no longer exists
- [ ] After rollback, `advisory_status` table is restored and `status_id` column is restored

## Verification Commands
- `cargo run -p migration -- up` — migration applies successfully
- `cargo run -p migration -- down` — migration rolls back successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
