# Task 2: Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of that enum type to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) drop the `status_id` foreign key column; and (5) drop the `advisory_status` table. All steps must execute within a single transaction so a failure at any point rolls back the entire migration.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration module implementing up/down for the enum conversion

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migrator
- `migration/Cargo.toml` -- add any required dependencies for enum type support if needed

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration conventions.

The `up` function should execute these steps in order:
1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
3. `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
5. `ALTER TABLE advisory DROP COLUMN status_id`
6. `DROP TABLE advisory_status`

The `down` function must reverse all steps to restore the lookup table and foreign key.

Per CONVENTIONS.md Key Conventions: use SeaORM migration patterns.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's migration file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with four values
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` from the existing `status_id` join in the same transaction
- [ ] Migration drops `status_id` foreign key column after backfill
- [ ] Migration drops `advisory_status` table after all references are removed
- [ ] Migration is fully reversible -- `down` restores the lookup table, foreign key, and data
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies cleanly against a fresh database with existing advisory data
- [ ] Migration rolls back cleanly, restoring the `advisory_status` table and `status_id` column
- [ ] Backfilled `status` values match the original `advisory_status.name` values

## Verification Commands
- `cargo run --bin migration -- up` -- migration applies without error
- `cargo run --bin migration -- down` -- migration rolls back without error

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

## additional_fields
- **labels**: ai-generated-jira, workflow:feature-branch
- **priority**: High
- **fixVersions**: RHTPA 2.0.0
