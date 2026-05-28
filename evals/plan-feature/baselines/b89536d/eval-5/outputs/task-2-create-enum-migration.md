## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`); (4) drop the `status_id` foreign key column from the `advisory` table; (5) drop the `advisory_status` table. All steps must be in a single transaction so a failure at any point rolls back the entire migration.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing the enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes
- Follow the migration pattern established in `migration/src/m0001_initial/mod.rs` for structure and SeaORM migration trait implementation.
- The migration must be reversible: the `down` method should recreate the `advisory_status` table, add back the `status_id` FK column, backfill from the enum column, and drop the `status` column and enum type.
- Use `sea_orm_migration::prelude::*` and implement the `MigrationTrait` for the new migration.
- The backfill step must handle the mapping between the old `advisory_status.id` integer values and the new enum string values.
- Ensure the migration is safe to run while the application is serving traffic (zero downtime requirement from the feature spec). Consider using `ALTER TABLE ... ADD COLUMN ... DEFAULT` to avoid full table rewrites on supported PostgreSQL versions.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration that demonstrates the project's migration pattern, table creation syntax, and SeaORM migration trait implementation

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration backfills the `status` column from the existing `advisory_status` lookup table join
- [ ] Migration drops the `status_id` foreign key column from the `advisory` table
- [ ] Migration drops the `advisory_status` table
- [ ] Migration is atomic — all steps are in a single transaction
- [ ] Migration is reversible — the `down` method restores the previous schema

## Test Requirements
- [ ] Migration runs successfully against a test database with existing advisory data
- [ ] Migration rollback (`down`) restores the `advisory_status` table and `status_id` FK column
- [ ] Verify that advisory rows retain their correct status values after migration

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
