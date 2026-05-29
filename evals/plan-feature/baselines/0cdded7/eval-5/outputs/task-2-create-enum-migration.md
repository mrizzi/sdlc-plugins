# Task 2 -- Create database migration for advisory_status_enum

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must: define the `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected), add a `status` column of that enum type to the `advisory` table, backfill the `status` column from the existing `advisory_status` join (`advisory.status_id` -> `advisory_status.id`), drop the `status_id` foreign key column, and drop the `advisory_status` table. The entire migration must be reversible and atomic -- if any step fails, all changes roll back.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- new migration module implementing the enum conversion

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration list
- `migration/Cargo.toml` -- add any additional dependencies if needed for enum type support

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and naming conventions
- Use SeaORM migration API (`MigrationTrait`, `up`/`down` methods) consistent with the existing `m0001_initial` migration
- The `up` method must execute all steps in order: (1) create enum type, (2) add column, (3) backfill, (4) drop FK column, (5) drop lookup table
- The `down` method must reverse all steps: (1) recreate lookup table, (2) add `status_id` FK column, (3) backfill `status_id` from enum, (4) drop `status` column, (5) drop enum type
- Use raw SQL for creating the PostgreSQL enum type since SeaORM's schema builder has limited enum support: `CREATE TYPE advisory_status_enum AS ENUM ('New', 'Analyzing', 'Fixed', 'Rejected')`
- The backfill step must use a single UPDATE statement joining `advisory` to `advisory_status` to populate the new column before dropping the old references
- Zero-downtime requirement: the migration adds the new column and backfills before dropping the old column, so reads using either the old join or the new column will work during the migration window
- Per docs/constraints.md SS2 (Commit Rules): commit message must follow Conventional Commits format and reference TC-9005

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration pattern to follow for structure, naming, and SeaORM migration trait implementation

## Acceptance Criteria
- [ ] Migration `up` creates `advisory_status_enum` type with exactly four values: New, Analyzing, Fixed, Rejected
- [ ] Migration `up` adds `status` column of type `advisory_status_enum` to `advisory` table
- [ ] Migration `up` backfills `status` column from existing `status_id` join
- [ ] Migration `up` drops `status_id` foreign key column from `advisory` table
- [ ] Migration `up` drops `advisory_status` lookup table
- [ ] Migration `down` reverses all changes and restores the original schema
- [ ] Migration is atomic -- partial failure rolls back all changes
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Run migration `up` against a test database with existing advisory data and verify all advisories have correct enum status values
- [ ] Run migration `down` after `up` and verify the original schema is fully restored
- [ ] Verify that running the migration on a database with no advisories succeeds without errors

## Verification Commands
- `cargo run -p migration -- up` -- migration completes without errors
- `cargo run -p migration -- down` -- rollback completes without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:dc259ec7727ccdf27046d9ca26b7f4fd02fc6706fc6a501c7133c837743ef1b5
