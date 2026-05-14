# Task 2 — Create database migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be reversible and atomic: if any step fails, the entire migration rolls back. The migration performs the following steps in order:

1. Create the PostgreSQL enum type `advisory_status_enum` with values (`New`, `Analyzing`, `Fixed`, `Rejected`)
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`)
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing the enum column migration with up and down functions

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migrator
- `migration/Cargo.toml` — Add any necessary dependencies if required

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions
- Use SeaORM's migration API (`sea_orm_migration::prelude::*`) for schema operations
- The `up` function must execute all five steps (create enum, add column, backfill, drop FK, drop table) within a single migration
- The `down` function must reverse the migration: recreate the `advisory_status` table, repopulate it, add the `status_id` FK column back, backfill `status_id` from the enum column, and drop the `status` column and enum type
- Use raw SQL via `manager.get_connection().execute_unprepared()` for the backfill step and enum type creation, as SeaORM's schema builder has limited support for PostgreSQL enum types
- The migration must be safe to run while the application is serving traffic (zero downtime requirement per feature NFRs)
- Per docs/constraints.md §2: commits must reference Jira issue ID, follow Conventional Commits, and include AI attribution trailer
- Per docs/constraints.md §3: branch must be named after the Jira issue ID, PR must specify `--base TC-9005`

## Acceptance Criteria
- [ ] Migration `up` function creates `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration `up` function adds `status` enum column to `advisory` table
- [ ] Migration `up` function backfills `status` from existing `advisory_status` join
- [ ] Migration `up` function drops `status_id` foreign key column from `advisory`
- [ ] Migration `up` function drops `advisory_status` table
- [ ] Migration `down` function fully reverses all changes
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Verify migration runs successfully against a clean database (up then down then up)
- [ ] Verify backfill correctly maps all existing status_id values to enum values
- [ ] Verify rollback (down) correctly restores the advisory_status table and status_id column

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
