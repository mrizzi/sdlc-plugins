## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: create the `advisory_status_enum` type, add a `status` enum column, backfill it from the existing `status_id` join, drop the `status_id` foreign key column, and drop the `advisory_status` table. The down migration must reverse all steps.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration that creates the enum type, adds the column, backfills data, drops the FK column, and drops the lookup table

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation
- Use `sea_orm_migration::prelude::*` and implement `MigrationTrait` with `up` and `down` methods
- In the `up` migration:
  1. Create the PostgreSQL enum type `advisory_status_enum` with values `'new'`, `'analyzing'`, `'fixed'`, `'rejected'` using raw SQL via `manager.get_connection().execute_unprepared()`
  2. Add column `status` of type enum to the `advisory` table with a default value
  3. Backfill the `status` column from the `advisory_status` table join: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
  4. Drop the `status_id` foreign key constraint
  5. Drop the `status_id` column from `advisory`
  6. Drop the `advisory_status` table
- In the `down` migration, reverse all steps: recreate the lookup table, add `status_id` column, backfill from enum, drop enum column, drop enum type
- The migration must be safe to run while the application is serving traffic (zero downtime requirement)
- Use raw SQL statements for enum type creation and backfill since SeaORM's schema builder has limited enum support for PostgreSQL
- Reference `common/src/db/query.rs` for any shared database utilities

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration demonstrating the project's SeaORM migration pattern and module structure

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` is created with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory.status` column exists with enum type, populated from existing data
- [ ] `advisory.status_id` column and its foreign key constraint are removed
- [ ] `advisory_status` table is dropped
- [ ] Down migration successfully reverses all changes
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing advisory data (backfill correctness)
- [ ] Down migration successfully reverts all changes
- [ ] Verify all four enum values are correctly mapped during backfill

## Verification Commands
- `cargo test -p migration` — migration compiles and passes any migration tests
- `cargo build -p migration` — migration crate builds without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main


[sdlc-workflow] Description digest: sha256:7f98f6fde1923a5a128d67e57eb27d69f9a0b6867051fe9d764607e3edde446e
