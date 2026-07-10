## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM database migration that atomically replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the new `status` column from the existing `advisory_status` table via the `status_id` foreign key; (4) drop the `status_id` foreign key column from the `advisory` table; (5) drop the `advisory_status` lookup table. All steps must execute within a single migration so that a failure at any point rolls back the entire change.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration implementing enum type creation, column addition, data backfill, FK column drop, and lookup table drop

## Implementation Notes
Follow the existing migration structure in `migration/src/m0001_initial/mod.rs` for file layout and migration trait implementation.

Use SeaORM's `MigrationTrait` with `up` and `down` methods. The `up` method must execute all five steps in order within the same migration. The `down` method must reverse the migration: recreate the `advisory_status` table, add the `status_id` FK column back, backfill from the enum column, drop the `status` enum column, and drop the `advisory_status_enum` type.

Use raw SQL via `manager.get_connection().execute_unprepared()` for the PostgreSQL enum type creation (`CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`) since SeaORM's schema manager does not have native enum type support.

For the backfill step, use an `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum` to populate the new column from the existing lookup table before dropping the FK.

Set the `status` column as `NOT NULL` after the backfill completes to prevent null values.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all error-producing operations.
Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration implementation demonstrating the migration trait pattern, file structure, and up/down method signatures

## Acceptance Criteria
- [ ] The migration creates the `advisory_status_enum` PostgreSQL type with values `New`, `Analyzing`, `Fixed`, `Rejected`
- [ ] The migration adds a `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] The migration backfills the `status` column from the existing `advisory_status` lookup table via `status_id`
- [ ] The migration drops the `status_id` foreign key column from the `advisory` table
- [ ] The migration drops the `advisory_status` lookup table
- [ ] The migration is reversible: `down` restores the original schema with lookup table and FK
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] All steps execute atomically within a single migration

## Test Requirements
- [ ] Migration `up` succeeds on a database with existing advisory rows that have valid `status_id` references
- [ ] Migration `down` restores the original schema and data
- [ ] Migration `up` fails cleanly (rolls back) if any advisory row has a null or invalid `status_id`
- [ ] After `up`, the `advisory` table has a `status` column with correct enum values matching the original lookup table values

## Verification Commands
- `cargo build -p migration` — migration module compiles without errors
- `cargo test -p migration` — migration tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
