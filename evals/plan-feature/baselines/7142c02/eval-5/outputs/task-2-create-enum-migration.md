## Repository
trustify-backend

## Target Branch
TC-9005

## Jira Metadata
- Priority: High
- Fix Version: RHTPA 2.0.0

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must create the `advisory_status_enum` type, add the `status` column, backfill values from the existing `status_id` foreign key join, drop the `status_id` column, and drop the `advisory_status` table. The migration must be atomic — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — Migration module for advisory status enum conversion

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and registration
- The migration must execute these steps in order within a single transaction:
  1. Create enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. Add column: `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. Backfill: `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`
  4. Set NOT NULL: `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
  5. Drop FK: `ALTER TABLE advisory DROP COLUMN status_id`
  6. Drop table: `DROP TABLE advisory_status`
- The down migration must reverse all steps: recreate the `advisory_status` table, add `status_id` column, backfill from enum, drop the enum column, and drop the enum type
- Use SeaORM migration traits (`MigrationTrait`, `up`, `down` methods)
- Per CONVENTIONS.md §Module pattern: follow the `model/ + service/ + endpoints/` module structure convention for any new module organization. Applies: task modifies `migration/src/lib.rs` matching the convention's Rust file scope.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` column to `advisory` table and backfills from existing `status_id` join
- [ ] Migration drops `status_id` foreign key column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] Migration is fully reversible — down migration restores the lookup table, FK column, and drops the enum
- [ ] Migration is atomic — partial failure rolls back all changes

## Test Requirements
- [ ] Migration runs successfully against a fresh database (up migration)
- [ ] Down migration successfully reverses all changes
- [ ] Backfill correctly maps all existing status values from the lookup table to enum values
- [ ] Migration handles edge cases: empty advisory table, advisories with all status types

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:e496cb2c98acab3147a829b97ec8ae7dfbd9341f5c112ebcefa0ff8ffc9c05fc
