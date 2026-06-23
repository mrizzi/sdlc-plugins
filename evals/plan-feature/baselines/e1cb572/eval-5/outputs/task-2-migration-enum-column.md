# Task 2 — Add database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: (1) create the `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) drop the `status_id` foreign key column; (5) drop the `advisory_status` table. All steps execute within a single transaction so any failure rolls back the entire operation.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- new migration module implementing the enum type creation, column addition with backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration runner

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for the migration struct and `MigrationTrait` implementation.

The migration `up()` must execute these steps in order within a single transaction:

1. Create the PostgreSQL enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. Add column `status` of type `advisory_status_enum` to the `advisory` table (initially nullable)
3. Backfill: `UPDATE advisory SET status = (SELECT name::advisory_status_enum FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
4. Set `status` column to `NOT NULL` after backfill completes
5. Drop the foreign key constraint on `advisory.status_id`
6. Drop the `status_id` column from `advisory`
7. Drop the `advisory_status` table

The `down()` method must reverse the migration: recreate the `advisory_status` table with its original rows, re-add the `status_id` FK column, backfill it from the enum column, drop the `status` column, and drop the enum type.

Use `manager.get_connection().execute_unprepared()` for raw SQL statements, as SeaORM's schema builder does not natively support PostgreSQL enum type creation. The migration must be safe to run while the application is serving traffic (zero downtime requirement). Use a single bulk UPDATE for the backfill rather than row-by-row processing.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration pattern to follow for struct definition and `MigrationTrait` implementation

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` is created with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory` table has a new `status` column of type `advisory_status_enum`
- [ ] All existing rows in `advisory` have their `status` column correctly backfilled from the `advisory_status` join
- [ ] The `status_id` FK column is dropped from the `advisory` table
- [ ] The `advisory_status` lookup table is dropped
- [ ] The migration is reversible: `down()` restores the previous schema
- [ ] The migration runs atomically -- partial failure rolls back all changes
- [ ] The migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies successfully against a test database with existing advisory rows that have `status_id` references
- [ ] After migration, `advisory.status` column contains correct enum values matching prior `advisory_status` names
- [ ] After migration, `advisory_status` table no longer exists
- [ ] Down migration restores the `advisory_status` table and `status_id` column with correct data

## Verification Commands
- `cargo run --bin migration -- up` -- migration completes without error
- `cargo run --bin migration -- down` -- rollback completes without error

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

`[sdlc-workflow] Description digest: sha256-md:d7e2f4a1b8c3d5e6f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2`
