## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the new `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`); (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` table. The migration must be reversible and atomic — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing enum type creation, column addition, backfill, FK drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions. The migration must implement both `up` and `down` methods for reversibility. The `down` method should: recreate the `advisory_status` table, add back the `status_id` FK column, backfill `status_id` from the enum column, and drop the `status` column and enum type.

Use SeaORM's `sea_orm_migration::prelude::*` and the `extension::postgres::Type` for creating and dropping PostgreSQL enum types.

Ensure the migration is safe to run while the application is serving traffic (zero downtime requirement from the feature spec).

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join data
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible — `down` method restores the previous schema
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration `up` completes without error on a database with existing advisory data
- [ ] Migration `down` completes without error and restores the previous schema
- [ ] After `up`, the `advisory` table has a `status` column with correct enum values
- [ ] After `up`, the `advisory_status` table no longer exists
- [ ] After `up`, all existing advisories retain their correct status values

## Verification Commands
- `cargo test -p migration` — migration compiles and passes any migration-level tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:bacc8db974365723a8dfae8108e21546e463ff2352898c28e57c2ed318b0c6bb
