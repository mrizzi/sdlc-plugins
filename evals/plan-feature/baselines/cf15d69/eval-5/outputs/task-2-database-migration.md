## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that introduces the `advisory_status_enum` PostgreSQL enum type, adds a `status` enum column to the `advisory` table, backfills it from the existing `advisory_status` join, drops the `status_id` foreign key column, and drops the `advisory_status` lookup table. The migration must be atomic so that a failure at any step rolls back the entire change.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing `MigrationTrait` with `up()` and `down()` methods

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migrator's migration list

## Implementation Notes
- In `up()`:
  1. Create the enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. Add the column: `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. Backfill: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. Set NOT NULL: `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
  5. Drop the foreign key constraint on `advisory.status_id`
  6. Drop column: `ALTER TABLE advisory DROP COLUMN status_id`
  7. Drop table: `DROP TABLE advisory_status`
- In `down()`:
  1. Recreate the `advisory_status` table with `id` and `name` columns
  2. Insert the four status rows
  3. Add `status_id` column to `advisory` and backfill from the enum column
  4. Add the foreign key constraint
  5. Drop the `status` enum column
  6. Drop the `advisory_status_enum` type
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for SeaORM migration structure
- Wrap the entire migration in a transaction to satisfy the atomicity non-functional requirement

Per Key Conventions (Framework): Use SeaORM migration API (`sea_orm_migration::prelude::*`) for defining the migration. Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the migration module scope.

## Acceptance Criteria
- [ ] `advisory_status_enum` type exists in PostgreSQL with values New, Analyzing, Fixed, Rejected
- [ ] `advisory.status` column of type `advisory_status_enum` is populated and NOT NULL
- [ ] `advisory.status_id` column no longer exists
- [ ] `advisory_status` table no longer exists
- [ ] Migration is fully reversible — `down()` restores the original schema
- [ ] Migration is atomic — a failure at any step rolls back all changes

## Test Requirements
- [ ] Run the migration against a test database and verify the enum column exists with correct values
- [ ] Run `down()` and verify the original schema is restored (lookup table, foreign key, status_id column)
- [ ] Verify data integrity: all advisory rows have the correct status value after migration

## Verification Commands
```bash
cargo run -p migration -- up
cargo run -p migration -- down
```

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:99b15079075034459ccc5519e70e357972e965a1b3de70443c8d0de9dc43ea2e
