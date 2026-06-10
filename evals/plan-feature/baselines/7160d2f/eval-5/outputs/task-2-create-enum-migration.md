## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that: (1) creates the PostgreSQL enum type `advisory_status_enum` with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) adds a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfills the `status` column from the existing `advisory_status` lookup table via the `status_id` foreign key; (4) drops the `status_id` foreign key column from the `advisory` table; (5) drops the `advisory_status` lookup table. The migration must be reversible — the down migration should recreate the lookup table, re-add the foreign key column, and backfill from the enum column.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — atomic migration implementing all five steps (create enum, add column, backfill, drop FK, drop table)

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- The migration must be atomic: wrap all steps in a single `up` function so that if any step fails, the entire migration rolls back. This prevents partial migrations that would leave the database in an inconsistent state.
- Use SeaORM migration API (`sea_orm_migration::prelude::*`) for the migration.
- For the enum type creation, use raw SQL via `manager.get_connection().execute_unprepared()` since SeaORM does not have native enum type creation support: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`.
- For the backfill step, use a raw SQL `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)` to populate the new column from the existing lookup table before dropping the FK.
- The down migration should: recreate `advisory_status` table, repopulate it with the four status values, add `status_id` FK column back to `advisory`, backfill `status_id` from the enum column, and drop the `status` enum column and type.
- Per docs/constraints.md §2 (Commit Rules): commit must reference TC-9005 in footer, use Conventional Commits format, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing migration code before implementing; follow established patterns.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — reference for migration structure, table creation patterns, and SeaORM migration API usage

## Acceptance Criteria
- [ ] Migration `up` creates `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration `up` adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration `up` backfills `status` from the existing `advisory_status` join
- [ ] Migration `up` drops the `status_id` foreign key column from `advisory`
- [ ] Migration `up` drops the `advisory_status` lookup table
- [ ] Migration `down` reverses all changes (recreates table, FK, and backfills)
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] All five steps are atomic — partial failure rolls back the entire migration

## Test Requirements
- [ ] Run `cargo test` in the migration crate to verify compilation
- [ ] Verify the migration applies cleanly against a fresh database
- [ ] Verify the down migration reverses cleanly
- [ ] Verify that after `up`, the `advisory` table has a `status` column and no `status_id` column
- [ ] Verify that after `up`, the `advisory_status` table no longer exists

## Verification Commands
- `cargo build -p migration` — expected: compiles without errors
- `cargo test -p migration` — expected: all tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
