## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that transitions the advisory status storage from a lookup table to a PostgreSQL enum column. The migration must: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join (`UPDATE advisory SET status = advisory_status.name FROM advisory_status WHERE advisory.status_id = advisory_status.id`); (4) set the `status` column to NOT NULL after backfill; (5) drop the `status_id` foreign key column from `advisory`; (6) drop the `advisory_status` table. The down migration must reverse all steps.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing up/down for the enum status transition

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list
- `migration/Cargo.toml` — add any needed dependencies if required

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- The migration must be atomic: wrap all steps in a single transaction so a failure at any step rolls back the entire migration.
- For the enum type creation, use raw SQL via SeaORM's `ConnectionTrait::execute_unprepared()`:
  ```sql
  CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected');
  ```
- For the backfill step, use a single UPDATE statement joining `advisory_status` to populate the new `status` column before making it NOT NULL.
- The down migration must: recreate the `advisory_status` table, add back `status_id` column, backfill `status_id` from `status` values, drop the `status` column, and drop the `advisory_status_enum` type.
- Zero downtime consideration: the migration adds the new column and backfills before dropping the old column, ensuring no window where neither column exists.
- Per `docs/constraints.md` §2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005 in the footer.
- Per `docs/constraints.md` §3 (PR Rules): branch must be named after the Jira issue ID; PR must target the `TC-9005` feature branch.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration demonstrating the project's migration structure and patterns

## Acceptance Criteria
- [ ] `advisory_status_enum` PostgreSQL type is created with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory.status` column exists with type `advisory_status_enum` and is NOT NULL
- [ ] All existing advisory rows have `status` populated correctly from the former `status_id` join
- [ ] `advisory.status_id` column is dropped
- [ ] `advisory_status` table is dropped
- [ ] Down migration successfully reverses all changes
- [ ] Migration runs within a transaction (atomic rollback on failure)

## Test Requirements
- [ ] Run migration up against a test database with existing advisory data and verify `status` column is correctly populated
- [ ] Run migration down and verify the `advisory_status` table and `status_id` column are restored
- [ ] Verify that a partial failure (e.g., simulated error after enum creation but before backfill) rolls back cleanly

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main