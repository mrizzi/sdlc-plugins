# Task 2 — Create database migration for advisory status enum conversion

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that converts the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must:

1. Create the `advisory_status_enum` PostgreSQL enum type with values (`New`, `Analyzing`, `Fixed`, `Rejected`).
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table.
3. Backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`).
4. Drop the `status_id` foreign key column from the `advisory` table.
5. Drop the `advisory_status` lookup table.

The migration must be atomic (all steps in a single transaction) and reversible (the down migration recreates the lookup table, re-adds the FK column, and backfills from the enum column).

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing the enum conversion

## Implementation Notes
- Follow the existing migration structure in `migration/src/m0001_initial/mod.rs` for module organization and SeaORM migration API usage.
- Use `sea_orm_migration::prelude::*` and implement the `MigrationTrait` with `up` and `down` methods.
- For the PostgreSQL enum type creation, use raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM's migration API does not have built-in enum type support.
- The backfill must happen within the same migration transaction as the column addition — do not split across separate migrations.
- The `down` migration must reverse all steps: recreate `advisory_status` table, re-add `status_id` FK column, backfill from enum, drop enum column, drop enum type.
- Per CONVENTIONS.md §Framework: use SeaORM migration API for table and column operations.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's database framework scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the project's SeaORM migration pattern, table creation syntax, and module registration approach

## Acceptance Criteria
- [ ] The `advisory_status_enum` PostgreSQL enum type is created with values (`New`, `Analyzing`, `Fixed`, `Rejected`)
- [ ] The `advisory.status` column exists and is populated from the former `advisory_status` join
- [ ] The `advisory.status_id` FK column is dropped
- [ ] The `advisory_status` lookup table is dropped
- [ ] The migration is reversible — running `down` restores the previous schema
- [ ] The migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Run the migration `up` against a test database and verify the `advisory_status_enum` type exists
- [ ] Verify the `advisory.status` column is populated correctly for all existing rows
- [ ] Verify the `advisory_status` table no longer exists after migration
- [ ] Run the migration `down` and verify the previous schema is restored
- [ ] Verify the migration handles an empty `advisory` table without errors

## Verification Commands
- `cargo run -p migration -- up` — migration completes without errors
- `cargo run -p migration -- down` — rollback completes without errors
- `psql -c "SELECT enum_range(NULL::advisory_status_enum);"` — returns `{New,Analyzing,Fixed,Rejected}`

## Documentation Updates
- `README.md` — add a note about the schema change from lookup table to enum column in the database section, if one exists

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
