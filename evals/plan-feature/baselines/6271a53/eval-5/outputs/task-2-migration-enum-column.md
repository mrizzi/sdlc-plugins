## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic and reversible: create the `advisory_status_enum` type, add the `status` enum column, backfill it from the existing `status_id` join, drop the `status_id` foreign key column, and drop the `advisory_status` table. The down migration must reverse all steps to restore the original schema.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- New migration module implementing the enum column migration

## Files to Modify
- `migration/src/lib.rs` -- Register the new migration module in the migrator
- `migration/Cargo.toml` -- Add any additional dependencies if needed for enum type support

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions
- The migration must execute in a single transaction to satisfy the atomicity requirement: if any step fails, all changes roll back
- Use `sea_orm_migration::prelude::*` extension types for creating the PostgreSQL enum
- Migration steps in order: (1) CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected'), (2) ALTER TABLE advisory ADD COLUMN status advisory_status_enum, (3) UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id), (4) ALTER TABLE advisory ALTER COLUMN status SET NOT NULL, (5) ALTER TABLE advisory DROP COLUMN status_id, (6) DROP TABLE advisory_status
- The down migration must reverse these steps: recreate `advisory_status` table, add `status_id` column, backfill from enum, drop enum column, drop enum type
- Per the feature's non-functional requirements: migration must be safe to run while the application is serving traffic (zero downtime)

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- Existing migration showing the project's migration patterns and conventions

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration backfills `status` column from the existing `advisory_status` join
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is fully reversible (down migration restores the original schema)
- [ ] Migration is atomic -- partial failure rolls back all changes

## Test Requirements
- [ ] Run migration up and verify the `advisory` table has a `status` enum column and no `status_id` column
- [ ] Run migration down and verify the original schema is restored (advisory_status table, status_id FK column)
- [ ] Verify the migration handles the case where advisory rows exist with valid status_id values
- [ ] Verify migration fails cleanly if an advisory has a status_id that does not exist in the advisory_status table

## Verification Commands
- `cargo run -p migration -- up` -- migration applies successfully
- `cargo run -p migration -- down` -- migration rolls back successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
