# Task 2 — Create migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible SeaORM database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic: if any step fails, the entire migration rolls back. The migration must be safe to run while the application is serving traffic (zero downtime).

The migration performs the following steps in order:
1. Create the `advisory_status_enum` PostgreSQL enum type with values: `New`, `Analyzing`, `Fixed`, `Rejected`
2. Add a `status` column of type `advisory_status_enum` to the `advisory` table (initially nullable for backfill)
3. Backfill `status` from the existing `advisory_status` join: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
4. Set the `status` column to NOT NULL after backfill
5. Drop the `status_id` foreign key constraint from `advisory`
6. Drop the `status_id` column from `advisory`
7. Drop the `advisory_status` table

The down migration must reverse these steps: recreate the `advisory_status` table, re-add `status_id`, backfill from enum, drop `status` column, and drop the enum type.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — the migration module implementing the enum type creation, column addition, backfill, FK/column drop, and table drop

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migrator

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- Use SeaORM's `sea_orm_migration::prelude::*` for the migration traits.
- The PostgreSQL enum type must be created using raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM's schema manager does not natively support `CREATE TYPE ... AS ENUM`.
- For the backfill step, use `UPDATE advisory SET status = ast.name FROM advisory_status ast WHERE ast.id = advisory.status_id` to populate the new column from the lookup table in a single statement.
- The migration must be wrapped in a transaction for atomicity — SeaORM migrations run inside a transaction by default, but verify this applies for raw SQL statements.
- For zero-downtime safety: adding a nullable column, backfilling, then setting NOT NULL is the standard safe pattern. The `DROP COLUMN` and `DROP TABLE` steps only execute after the backfill is confirmed complete.
- Per docs/constraints.md §5.2: inspect `migration/src/m0001_initial/mod.rs` before implementing to follow established patterns.

## Acceptance Criteria
- [ ] The `advisory_status_enum` PostgreSQL enum type is created with values (New, Analyzing, Fixed, Rejected)
- [ ] The `advisory.status` column exists with type `advisory_status_enum` and NOT NULL constraint
- [ ] All existing advisory rows have `status` populated from their former `status_id` values
- [ ] The `advisory.status_id` column and its foreign key constraint are dropped
- [ ] The `advisory_status` table is dropped
- [ ] The migration is reversible (down migration recreates the lookup table and restores `status_id`)
- [ ] The migration is atomic (partial failure rolls back all changes)

## Test Requirements
- [ ] Run the up migration against a test database with seeded advisory data and verify the `status` column is populated correctly
- [ ] Run the down migration and verify the `advisory_status` table and `status_id` column are restored
- [ ] Verify that running up then down then up produces a consistent schema (idempotency)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error
- `psql -c "SELECT status, count(*) FROM advisory GROUP BY status"` — all rows have a valid enum value

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
