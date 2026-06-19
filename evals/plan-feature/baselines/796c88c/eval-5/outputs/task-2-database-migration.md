## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create the database migration that replaces the `advisory_status` lookup table with a PostgreSQL enum column on the `advisory` table. The migration must be atomic: create the enum type, add the column, backfill existing rows from the `status_id` join, drop the foreign key column, and drop the lookup table -- all within a single transaction so that a failure at any step rolls back the entire migration.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- Migration module implementing the enum type creation, column addition, backfill, FK column drop, and lookup table drop

## Files to Modify
- `migration/src/lib.rs` -- Register the new migration module in the migrator
- `migration/Cargo.toml` -- Add any required dependencies for the migration

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation
- The migration must execute all steps within a single transaction to satisfy the atomicity requirement
- Create the PostgreSQL enum type `advisory_status_enum` with values: `New`, `Analyzing`, `Fixed`, `Rejected`
- Add column `status` of type `advisory_status_enum` to the `advisory` table
- Backfill the `status` column using a SQL UPDATE with JOIN: `UPDATE advisory SET status = s.name::advisory_status_enum FROM advisory_status s WHERE advisory.status_id = s.id`
- After backfill, set the `status` column to NOT NULL
- Drop the `status_id` foreign key constraint and column from `advisory`
- Drop the `advisory_status` table
- Include a reversible down migration that recreates the lookup table and FK column

## Acceptance Criteria
- [ ] Migration creates `advisory_status_enum` PostgreSQL enum type with values (New, Analyzing, Fixed, Rejected)
- [ ] Migration adds `status` enum column to `advisory` table and backfills from `status_id` join
- [ ] Migration drops `status_id` FK column from `advisory` table
- [ ] Migration drops `advisory_status` lookup table
- [ ] All migration steps execute within a single transaction (atomic rollback on failure)
- [ ] Down migration reverses all changes

## Test Requirements
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing advisory data
- [ ] Migration rolls back cleanly if any step fails
- [ ] Down migration restores the original schema

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
