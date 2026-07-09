## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must:

1. Create the `advisory_status_enum` type with values (`New`, `Analyzing`, `Fixed`, `Rejected`)
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table
3. Backfill the `status` column from the existing `status_id` foreign key join with `advisory_status`
4. Drop the `status_id` foreign key column from the `advisory` table
5. Drop the `advisory_status` lookup table

The migration must be atomic -- if any step fails, the entire migration rolls back. The down migration must reverse all steps to restore the original schema.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- migration module implementing up/down for enum type conversion

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migrator
- `migration/Cargo.toml` -- add any required dependencies for enum type support

## Implementation Notes
- Use SeaORM migration framework (`MigrationTrait`) to define the `up` and `down` functions.
- In the `up` function, use raw SQL via `manager.get_connection().execute_unprepared()` for creating the enum type, adding the column with backfill, and dropping the FK and table, all within the migration transaction.
- The backfill step should use `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum` or equivalent SQL.
- The `down` function must: recreate the `advisory_status` table, repopulate it with the four status values, add `status_id` column with FK, backfill `status_id` from the enum column, drop the `status` enum column, and drop the `advisory_status_enum` type.
- Per CONVENTIONS.md §Framework: use SeaORM migration patterns for database schema changes.
  Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's SeaORM migration file scope.
- Reference existing migration at `migration/src/m0001_initial/mod.rs` for the established migration structure and transaction pattern.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration module demonstrating the SeaORM `MigrationTrait` pattern, table creation, and transaction structure

## Acceptance Criteria
- [ ] Migration `up` creates `advisory_status_enum` type with four values (New, Analyzing, Fixed, Rejected)
- [ ] Migration `up` adds `status` enum column to `advisory` table
- [ ] Migration `up` backfills `status` from `status_id` join with `advisory_status`
- [ ] Migration `up` drops `status_id` FK column from `advisory` table
- [ ] Migration `up` drops `advisory_status` lookup table
- [ ] Migration `down` fully reverses all changes and restores original schema
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration is atomic -- partial failure rolls back all changes

## Test Requirements
- [ ] Run migration up against a test database with seeded advisory data and verify enum column is populated correctly
- [ ] Run migration down and verify original schema is restored with data intact
- [ ] Verify migration handles empty `advisory` table without error
- [ ] Verify migration handles all four status values during backfill

## Verification Commands
- `cargo test -p migration` -- migration tests pass
- `sea-orm-cli migrate up` -- migration applies successfully against test database

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
