# Task 2 — Create database migration: advisory_status enum column and drop lookup table

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible SeaORM database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic (all steps succeed or all roll back) and safe to run while the application is serving traffic (zero downtime). This migration is the foundational change that all other tasks in this feature depend on.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum conversion

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the module structure and registration approach.
- The migration must perform these steps in order within a single transaction:
  1. Create the PostgreSQL enum type `advisory_status_enum` with values: `'New'`, `'Analyzing'`, `'Fixed'`, `'Rejected'`
  2. Add a new column `status` of type `advisory_status_enum` to the `advisory` table (initially nullable to support backfill)
  3. Backfill the `status` column from the existing `advisory_status` join: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. Set the `status` column to NOT NULL after backfill
  5. Drop the `status_id` foreign key constraint from the `advisory` table
  6. Drop the `status_id` column from the `advisory` table
  7. Drop the `advisory_status` table
- The down migration must reverse all steps: recreate the `advisory_status` table, re-add the `status_id` column with FK, backfill from the enum column, drop the enum column, and drop the enum type.
- Use SeaORM's `sea_query` to construct the DDL statements. For the enum type creation, use raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM does not have native PostgreSQL enum type creation support.
- Ensure the migration is idempotent where possible — check for existence before creating types.

## Acceptance Criteria
- [ ] Migration creates the `advisory_status_enum` PostgreSQL type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` enum column to `advisory` table and backfills it from the existing `status_id` join
- [ ] Migration drops the `status_id` column and its foreign key constraint
- [ ] Migration drops the `advisory_status` table
- [ ] The entire migration is atomic — if any step fails, all changes roll back
- [ ] The down migration fully reverses the up migration, restoring the original schema
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration up against a test database with sample advisory data and verify: enum type exists, `status` column is populated correctly, `status_id` column is gone, `advisory_status` table is gone
- [ ] Run migration down and verify the original schema is fully restored with data intact
- [ ] Verify migration handles the case where advisories exist with all four status values

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `sea-orm-cli migrate up` — migration applies successfully
- `sea-orm-cli migrate down` — migration rolls back successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
