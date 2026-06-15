## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must create the enum type, add the new column, backfill existing rows, drop the foreign key, and drop the lookup table — all within a single transaction so that any failure rolls back the entire operation.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — New migration module implementing the full enum migration

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner
- `migration/Cargo.toml` — Add any required dependencies for enum type support if needed

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and migration trait implementation.

The migration should execute these steps in order within a single transaction:
1. `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
3. `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum` to backfill from the lookup table join
4. `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL` after backfill
5. `ALTER TABLE advisory DROP CONSTRAINT` on the `status_id` foreign key
6. `ALTER TABLE advisory DROP COLUMN status_id`
7. `DROP TABLE advisory_status`

The down migration should reverse these steps: recreate the lookup table, add `status_id` column, backfill from enum, drop enum column, drop enum type.

Register the new migration in `migration/src/lib.rs` following the pattern used for `m0001_initial`.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with values New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` from the existing `advisory_status` lookup join
- [ ] Migration sets `status` column as NOT NULL after backfill
- [ ] Migration drops the `status_id` foreign key column from `advisory`
- [ ] Migration drops the `advisory_status` table
- [ ] All steps execute within a single transaction (atomic rollback on failure)
- [ ] Down migration reverses all changes

## Test Requirements
- [ ] Run migration up against a test database with existing advisory rows and verify enum column is populated correctly
- [ ] Run migration down and verify the lookup table and foreign key are restored
- [ ] Verify migration rolls back cleanly if any step fails (e.g., simulate failure after enum creation)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005

[sdlc-workflow] Description digest: sha256-md:3862f59f55b7614f922f9ba28a7283fbdce615ece62081bf7c08c246b6114c83
