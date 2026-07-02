## Summary
Create database migration to replace advisory_status table with enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a SeaORM migration that atomically replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must create the `advisory_status_enum` type with values (New, Analyzing, Fixed, Rejected), add a `status` enum column to `advisory`, backfill it from the existing `status_id` join, drop the `status_id` foreign key column, and drop the `advisory_status` table. All steps must execute within a single transaction so that a failure at any point rolls back the entire migration.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- Migration module that creates the enum type, adds the column, backfills data, drops the foreign key, and drops the lookup table

## Files to Modify
- `migration/src/lib.rs` -- Register the new migration module in the migrator
- `migration/Cargo.toml` -- Add any required dependencies for enum support if needed

## Implementation Notes
Per CONVENTIONS.md §Migration Patterns: implement the migration using SeaORM's `MigrationTrait` with `up()` and `down()` methods; the `down()` method must reverse all changes to make the migration reversible. Applies: task creates `migration/src/m0002_advisory_status_enum/mod.rs` matching the convention's `.rs` migration file scope.

The migration must:
1. Create the `advisory_status_enum` PostgreSQL enum type
2. Add `status` column of type `advisory_status_enum` to `advisory` table
3. Execute a backfill: `UPDATE advisory SET status = (SELECT name FROM advisory_status WHERE id = advisory.status_id)`
4. Set `status` column to NOT NULL after backfill
5. Drop the `status_id` foreign key constraint and column from `advisory`
6. Drop the `advisory_status` table
7. Drop the `advisory_status_enum` type in `down()`

Reference the existing migration structure in `migration/src/m0001_initial/mod.rs` for the migration pattern.

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` type with values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds `status` enum column to `advisory` table
- [ ] Migration backfills `status` from the existing `status_id` join
- [ ] Migration drops `status_id` column and foreign key from `advisory`
- [ ] Migration drops the `advisory_status` table
- [ ] Migration is fully reversible via `down()`
- [ ] All steps execute within a single transaction (atomic rollback on failure)

## Test Requirements
- [ ] Migration `up()` succeeds on a fresh database with seeded advisory_status data
- [ ] Migration `down()` restores the advisory_status table and status_id column
- [ ] Backfill correctly maps all existing status_id values to enum values
- [ ] Migration rolls back cleanly if any step fails

## Verification Commands
- `cargo run --bin migration -- up` -- migration applies successfully
- `cargo run --bin migration -- down` -- migration reverses successfully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

## Additional Fields
- priority: High
- fixVersions: RHTPA 2.0.0
- labels: ai-generated-jira
