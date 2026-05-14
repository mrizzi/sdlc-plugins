# Task 2 -- Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must perform five steps in a single transaction: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` table. The migration must be reversible -- the down migration recreates the lookup table and foreign key.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- New migration module implementing the enum migration with up and down functions

## Files to Modify
- `migration/src/lib.rs` -- Register the new `m0002_advisory_status_enum` migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- Use `sea_orm_migration::prelude::*` and implement `MigrationTrait` with `up` and `down` methods.
- In the `up` method, use raw SQL via `manager.get_connection().execute_unprepared()` to:
  1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
  5. `ALTER TABLE advisory DROP COLUMN status_id`
  6. `DROP TABLE advisory_status`
- In the `down` method, reverse the steps: recreate `advisory_status` table, populate with the four status values, add `status_id` column, backfill from enum, drop `status` column, drop enum type.
- Register the module in `migration/src/lib.rs` by adding it to the `vec![]` of migrations returned by the `Migrator` struct, following the pattern of the existing `m0001_initial` entry.
- The migration crate's `Cargo.toml` is at `migration/Cargo.toml`; no dependency changes are needed since SeaORM migration already provides the required functionality.

## Acceptance Criteria
- [ ] Migration module `m0002_advisory_status_enum` exists and is registered in `migration/src/lib.rs`
- [ ] `up` migration creates enum type, adds column, backfills, makes column NOT NULL, drops `status_id`, drops `advisory_status` table
- [ ] `down` migration reverses all changes (recreates table, repopulates, adds FK column, drops enum)
- [ ] Migration compiles without errors (`cargo build -p migration`)
- [ ] Migration runs successfully against a test database with existing advisory data

## Test Requirements
- [ ] Run migration `up` on a test database with seeded advisory rows and verify `advisory.status` column contains correct enum values
- [ ] Run migration `down` and verify `advisory_status` table and `advisory.status_id` column are restored
- [ ] Verify that running `up` on an empty database (no advisory rows) succeeds without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
