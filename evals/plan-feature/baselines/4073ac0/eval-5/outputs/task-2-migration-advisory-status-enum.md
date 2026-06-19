## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic — if any step fails, the entire migration rolls back. Steps: create `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected); add `status` enum column to `advisory`; backfill `status` from the existing `status_id` join to `advisory_status`; drop the `status_id` foreign key column; drop the `advisory_status` table. The migration must also define a reversible down migration that recreates the lookup table, re-populates it, adds back the FK column, and backfills it.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — Migration module for advisory status enum conversion

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migrator

## Implementation Notes
Follow the migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and registration.

The migration must execute these steps within a single transaction:
1. Create enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
2. Add column: `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
3. Backfill: `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`
4. Set NOT NULL: `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
5. Drop FK column: `ALTER TABLE advisory DROP COLUMN status_id`
6. Drop lookup table: `DROP TABLE advisory_status`

The down migration must reverse all steps in the opposite order.

Register the new migration in `migration/src/lib.rs` following the existing `Migrator` vec pattern used for `m0001_initial`.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration backfills `status` from the existing `advisory_status` join
- [ ] Migration sets `status` column to NOT NULL after backfill
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is reversible (down migration recreates table and FK)
- [ ] All migration steps execute within a single transaction (atomic)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration up succeeds on a database with existing advisory rows that have status_id values
- [ ] After migration up, `advisory.status` contains correct enum values matching the original `advisory_status` names
- [ ] Migration down succeeds and restores the `advisory_status` table and `status_id` column
- [ ] Migration fails atomically if any intermediate step errors (e.g., unknown status value)

## Verification Commands
- `cargo run -p migration -- up` — migration applies without error
- `cargo run -p migration -- down` — migration rolls back without error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
