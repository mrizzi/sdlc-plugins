# Task 2 -- Create migration: add advisory_status_enum type, backfill status column, drop lookup table

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create a new SeaORM migration that performs the full schema transition from the `advisory_status` lookup table to an `advisory_status_enum` PostgreSQL enum column on the `advisory` table. The migration must be atomic (all-or-nothing) and reversible. It performs four steps in order: (1) create the `advisory_status_enum` PostgreSQL enum type with values `New`, `Analyzing`, `Fixed`, `Rejected`; (2) add a `status` column of type `advisory_status_enum` to the `advisory` table and backfill it from the existing `advisory_status` join; (3) drop the `status_id` foreign key column from the `advisory` table; (4) drop the `advisory_status` lookup table.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` -- new migration module implementing the enum type creation, column addition with backfill, FK column drop, and lookup table drop

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module in the migration runner
- `migration/Cargo.toml` -- add any new dependencies if needed for enum type support

## Implementation Notes
- The migration must wrap all four steps (create enum type, add+backfill column, drop FK column, drop table) in a single transaction to ensure atomicity. If any step fails, the entire migration rolls back.
- The `down()` method must reverse the migration: recreate the `advisory_status` table, re-add the `status_id` FK column, backfill it from the enum column, and drop the enum column and type.
- For the backfill step, use a SQL statement like: `UPDATE advisory SET status = (SELECT name::advisory_status_enum FROM advisory_status WHERE advisory_status.id = advisory.status_id)`
- Use SeaORM's `extension::postgres::Type` for creating the PostgreSQL enum type.
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the migration struct and `MigrationTrait` implementation.
- The migration must be safe to run while the application is serving traffic (zero downtime requirement). Since this is an atomic migration and PostgreSQL handles DDL in transactions, this is achievable as long as the migration completes quickly. The backfill should use a single UPDATE statement rather than row-by-row processing.

Per CONVENTIONS.md &sect;Framework: SeaORM for database -- use SeaORM migration traits and PostgreSQL extension types for enum creation.
Applies: task modifies `migration/src/lib.rs` matching the convention's migration module scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration pattern to follow for struct definition and `MigrationTrait` implementation

## Acceptance Criteria
- [ ] PostgreSQL enum type `advisory_status_enum` is created with values (New, Analyzing, Fixed, Rejected)
- [ ] `advisory` table has a new `status` column of type `advisory_status_enum`
- [ ] All existing rows in `advisory` have their `status` column correctly backfilled from the `advisory_status` join
- [ ] The `status_id` FK column is dropped from the `advisory` table
- [ ] The `advisory_status` lookup table is dropped
- [ ] The migration is reversible: `down()` restores the previous schema
- [ ] The migration runs atomically -- partial failure rolls back all changes

## Test Requirements
- [ ] Run the migration forward (`up`) against a test database with existing advisory rows and verify all four schema changes are applied
- [ ] Run the migration backward (`down`) and verify the original schema is restored with data intact
- [ ] Verify that the backfill correctly maps all four status values (New, Analyzing, Fixed, Rejected)

## Verification Commands
- `cargo run --bin migration -- up` -- migration completes without error
- `cargo run --bin migration -- down` -- rollback completes without error

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
