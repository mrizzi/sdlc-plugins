# Task 2 -- Create atomic migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM database migration that atomically replaces the `advisory_status` lookup table with a PostgreSQL `advisory_status_enum` type and a direct `status` column on the `advisory` table. The migration must be reversible and safe to run while the application is serving traffic. All steps (create enum type, add column, backfill, drop FK, drop table) must execute within a single transaction so a failure at any step rolls back the entire migration.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- new migration module implementing the enum migration

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration runner
- `migration/Cargo.toml` -- add any additional dependencies if needed for enum support

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and naming convention.
- The migration must perform these steps in order within a single transaction:
  1. Create the PostgreSQL enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. Add the `status` column to `advisory` table: `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. Backfill the `status` column from the join: `UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`
  4. Set `status` column to `NOT NULL` after backfill
  5. Drop the `status_id` foreign key constraint
  6. Drop the `status_id` column from `advisory`
  7. Drop the `advisory_status` table
- The down migration must reverse all steps: recreate the `advisory_status` table, add `status_id` column, backfill from enum, drop `status` column, drop enum type.
- Use SeaORM's `manager.get_connection()` to execute raw SQL for enum type creation, as SeaORM's schema manager does not natively support PostgreSQL enum types.
- Zero-downtime requirement: because all application code changes land in the same feature branch, the migration and code changes will deploy together. Ensure the migration is idempotent where possible (e.g., `CREATE TYPE IF NOT EXISTS`).

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from `advisory_status` table join
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is atomic -- partial failure rolls back all changes
- [ ] Down migration reverses all changes
- [ ] Migration module is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration up against a test database with sample advisory data and verify the `status` column is populated correctly
- [ ] Run migration down and verify the `advisory_status` table and `status_id` column are restored
- [ ] Verify that a partial failure (e.g., simulated error mid-migration) rolls back all changes leaving the database in its original state

## Verification Commands
- `cargo run -p migration -- up` -- migration completes without errors
- `cargo run -p migration -- down` -- down migration reverses changes cleanly

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
