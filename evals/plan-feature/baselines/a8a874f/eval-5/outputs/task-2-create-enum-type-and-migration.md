# Task 2: Create PostgreSQL enum type and migration to add status column

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Create a reversible SeaORM migration that defines the `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected), adds a `status` enum column to the `advisory` table, backfills it from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table. All steps must execute within a single transaction so that any failure rolls back the entire migration, preventing an inconsistent schema state.

## Acceptance Criteria

- A new migration module exists under `migration/src/` with an `up` function that:
  1. Creates `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected
  2. Adds `status` column of type `advisory_status_enum` to the `advisory` table
  3. Backfills `status` from the `advisory_status` table via the `status_id` foreign key
  4. Drops the `status_id` column from `advisory`
  5. Drops the `advisory_status` table
- The migration `down` function reverses all steps: re-creates the lookup table, re-adds `status_id`, backfills from enum, drops the enum column, and drops the enum type
- The entire migration runs inside a single transaction
- The migration is registered in `migration/src/lib.rs`

## Test Requirements

- Run the migration `up` against a test database and verify the `advisory` table has a `status` column of type `advisory_status_enum`
- Run the migration `down` and verify the `advisory_status` table and `status_id` column are restored
- Verify that a partial failure (simulated) causes the entire migration to roll back

## Files to Create

- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration module implementing up/down

## Files to Modify

- `migration/src/lib.rs` -- register the new migration module
- `migration/Cargo.toml` -- add any needed dependencies if required

## Implementation Notes

- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`
- Use SeaORM's `sea_orm_migration::prelude` for defining the migration
- The backfill SQL should use a CASE or direct join to map `status_id` values to enum values
- Ensure the migration is wrapped in a transaction block for atomicity
- The enum type name should be `advisory_status_enum` to avoid collision with the table name

## Dependencies

- Task 1: Create feature branch TC-9005 from main

[Description digest: sha256-md:b4f2e8d9c3a05f6712gd9b5e8c4f3a201d7e9f5b6c8d1e2f3a4b5c6d7e8f9a01 would be posted as a comment]
