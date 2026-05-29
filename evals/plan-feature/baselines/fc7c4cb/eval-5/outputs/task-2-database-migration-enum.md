# Task 2 — Create database migration for advisory status enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a reversible database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: (1) create the `advisory_status_enum` type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of this enum type to the `advisory` table; (3) backfill the `status` column from the existing `advisory_status` join; (4) drop the `status_id` foreign key column from `advisory`; (5) drop the `advisory_status` table. The migration must be atomic — if any step fails, the entire migration rolls back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — migration module implementing up/down for the enum conversion

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and registration.
- The migration `up` function should execute these steps in order within a single transaction:
  1. Create enum type: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
  2. Add column: `ALTER TABLE advisory ADD COLUMN status advisory_status_enum`
  3. Backfill: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE advisory_status.id = advisory.status_id)::advisory_status_enum`
  4. Set NOT NULL: `ALTER TABLE advisory ALTER COLUMN status SET NOT NULL`
  5. Drop FK constraint and column: `ALTER TABLE advisory DROP COLUMN status_id`
  6. Drop lookup table: `DROP TABLE advisory_status`
- The migration `down` function must reverse all steps: recreate the `advisory_status` table, repopulate it, add `status_id` column with FK, backfill from enum, drop the enum column, drop the enum type.
- Use SeaORM migration traits (`MigrationTrait`, `DbBackend`) consistent with `migration/Cargo.toml` dependencies.
- The migration must be safe to run while the application is serving traffic (zero downtime requirement).

## Acceptance Criteria
- [ ] Migration `up` creates the `advisory_status_enum` type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration `up` adds a NOT NULL `status` column of type `advisory_status_enum` to the `advisory` table
- [ ] Migration `up` correctly backfills the `status` column from the existing `advisory_status` join
- [ ] Migration `up` drops the `status_id` column from `advisory`
- [ ] Migration `up` drops the `advisory_status` table
- [ ] Migration `down` fully reverses all changes, restoring the original schema
- [ ] All migration steps execute within a single transaction (atomic rollback on failure)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration `up` against a test database with seeded advisory data and verify the `status` column is populated correctly
- [ ] Run migration `down` and verify the original schema is restored with data intact
- [ ] Verify that a failed step mid-migration rolls back all previous steps

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without errors
- `cargo run --bin migration -- down` — rollback completes without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:7381ed703fc7043796bbc625a8fb50170b914a354b179b49f9564d2e49e75563
