## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected; (2) add a `status` column of that enum type to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`); (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` table. The migration must be atomic and reversible — the down migration must recreate the lookup table, re-add the FK column, backfill it, and drop the enum column and type.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — new migration module implementing the enum migration

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- The migration must be fully reversible: the `down` function must recreate the `advisory_status` table with its original rows, re-add `status_id` FK column to `advisory`, backfill `status_id` from the enum column, drop the `status` column, and drop the `advisory_status_enum` type.
- Use SeaORM migration traits (`MigrationTrait`, `SchemaManager`) consistently with the existing migration.
- The enum type should be created using raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM does not have native enum type creation support.
- Ensure the migration is safe to run while the application is serving traffic (zero downtime requirement from the feature spec). Consider using `SET lock_timeout` to avoid long table locks.
- The backfill must handle NULL `status_id` values gracefully (default to 'New' or reject the migration if NULLs exist).

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern demonstrating the project's migration structure and conventions

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to the `advisory` table
- [ ] Migration backfills `status` column from the existing `advisory_status` join
- [ ] Migration drops `status_id` foreign key column from `advisory`
- [ ] Migration drops the `advisory_status` lookup table
- [ ] Down migration fully reverses all changes (recreates table, FK, backfills, drops enum)
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run the migration up and verify the enum type, column, and backfilled data exist
- [ ] Run the migration down and verify the lookup table, FK column, and backfilled data are restored
- [ ] Verify the migration handles edge cases (empty advisory table, all four status values present)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors
- `psql -c "SELECT enumlabel FROM pg_enum WHERE enumtypid = 'advisory_status_enum'::regtype ORDER BY enumsortorder;"` — returns New, Analyzing, Fixed, Rejected

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
