## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join (`advisory.status_id` -> `advisory_status.id`); (4) drop the `status_id` foreign key column; (5) drop the `advisory_status` table. The migration must be atomic — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration module structure and registration.
- Use SeaORM's migration API (`sea_orm_migration::prelude::*`) to define `up()` and `down()` functions.
- In `up()`: use raw SQL via `manager.get_connection().execute_unprepared()` to create the enum type (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`), add the column, backfill, and drop the old column and table — all within a single transaction.
- In `down()`: reverse the migration by recreating the `advisory_status` table, adding back the `status_id` column, backfilling from the enum, dropping the `status` column, and dropping the enum type.
- The migration must be safe to run while the application is serving traffic (zero downtime requirement). Since this is a coordinated change landing on a feature branch, the migration and code changes will be deployed together.
- Per constraints §2.1–2.3: commit must reference TC-9005, follow Conventional Commits, and include the AI assistance trailer.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` column from existing `advisory_status` join data
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is fully reversible — `down()` restores the original schema
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration runs successfully against a test database with existing advisory data
- [ ] Migration rollback (`down()`) restores the original schema with `advisory_status` table and `status_id` column
- [ ] Backfill correctly maps all existing status values from the lookup table to enum values

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:60abe88f87716aa64545c3d4d7c38aa76cd189a1520a3c31271e4e754145d0da
