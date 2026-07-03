## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Create an atomic database migration that replaces the advisory_status lookup table with a PostgreSQL enum column on the advisory table. The migration must execute all steps within a single transaction: create the advisory_status_enum type with values (New, Analyzing, Fixed, Rejected), add a status enum column to the advisory table, backfill the new column from the existing status_id foreign key join, drop the status_id foreign key column, and drop the advisory_status table. If any step fails, the entire migration rolls back to prevent an inconsistent database state.

## Files to Create
- `migration/src/m0002_advisory_status_enum/mod.rs` — atomic migration: create enum type, add column, backfill, drop FK, drop table

## Files to Modify
- `migration/src/lib.rs` — register the new m0002_advisory_status_enum migration module
- `migration/Cargo.toml` — add any required dependencies for enum support if needed

## Implementation Notes
- Follow the existing SeaORM migration pattern in `migration/src/m0001_initial/mod.rs` for migration module structure and registration
- Use `sea_query::extension::postgres::Type` for creating the PostgreSQL enum type
- The backfill step must use a single UPDATE statement joining advisory_status to populate the new column before dropping the FK
- Implement both `up()` and `down()` methods — the down migration should recreate the advisory_status table, repopulate it from the enum column, add the FK back, and drop the enum type
- All migration steps must run within the same transaction to satisfy the atomicity NFR

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating SeaORM migration structure and registration pattern

## Acceptance Criteria
- [ ] Migration creates advisory_status_enum type with values: New, Analyzing, Fixed, Rejected
- [ ] Migration adds status column of type advisory_status_enum to the advisory table
- [ ] Migration backfills the status column from the existing status_id join
- [ ] Migration drops the status_id foreign key column from the advisory table
- [ ] Migration drops the advisory_status lookup table
- [ ] Migration is atomic — all steps succeed or all roll back
- [ ] Migration is reversible — down() restores the previous schema
- [ ] Migration compiles and is registered in migration/src/lib.rs

## Test Requirements
- [ ] Migration runs forward successfully against a test database
- [ ] Migration runs backward (down) successfully, restoring the advisory_status table and FK
- [ ] Verify enum type exists after forward migration: SELECT typname FROM pg_type WHERE typname = 'advisory_status_enum'
- [ ] Verify advisory_status table does not exist after forward migration

## Verification Commands
- `cargo build -p migration` — migration module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
