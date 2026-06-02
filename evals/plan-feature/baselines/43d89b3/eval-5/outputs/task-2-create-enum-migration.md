## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that performs the full schema transition from the `advisory_status` lookup table to an `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The migration must be atomic — if any step fails, the entire migration rolls back. The migration performs these steps in order: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.value FROM advisory_status WHERE advisory.status_id = advisory_status.id`); (4) set `status` column to NOT NULL after backfill; (5) drop the `status_id` foreign key constraint and column from the `advisory` table; (6) drop the `advisory_status` table.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing the enum transition

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and registration. The migration must implement both `up` and `down` functions for reversibility. The `down` migration must: recreate the `advisory_status` table, add back the `status_id` column, backfill `status_id` from the enum column, drop the `status` column, and drop the `advisory_status_enum` type.

Use SeaORM migration traits (`MigrationTrait`, `SchemaManager`) consistent with the existing migration in `m0001_initial/mod.rs`.

Ensure the migration is safe for zero-downtime deployment — all operations should be wrapped in a single transaction to maintain atomicity.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` column from existing `status_id` join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` foreign key and column from `advisory` table
- [ ] Migration drops `advisory_status` table
- [ ] Migration is reversible — `down` function restores the original schema
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Migration `up` runs successfully against a database with the original schema and existing advisory rows
- [ ] Migration `down` runs successfully and restores the original schema
- [ ] After `up`, the `advisory` table has a `status` column with correct enum values
- [ ] After `up`, the `advisory_status` table no longer exists
- [ ] After `up`, the `status_id` column no longer exists on the `advisory` table

## Verification Commands
- `cargo run --bin migration -- up` — migration applies successfully
- `cargo run --bin migration -- down` — migration rolls back successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
