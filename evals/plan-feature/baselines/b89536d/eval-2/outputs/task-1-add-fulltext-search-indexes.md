# Task 1 — Add full-text search GIN indexes via database migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a SeaORM database migration that adds PostgreSQL full-text search support to the searchable entities. This includes adding `tsvector` generated columns and GIN indexes on the `sbom`, `advisory`, and `package` tables to enable efficient full-text search queries. This is the foundational change that subsequent search performance and relevance tasks depend on.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that adds tsvector columns and GIN indexes to sbom (on name/description fields), advisory (on title/description/severity fields), and package (on name/license fields)

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and naming conventions.
- Use PostgreSQL `tsvector` generated columns with `to_tsvector('english', coalesce(field1, '') || ' ' || coalesce(field2, ''))` to combine multiple searchable fields per table.
- Create GIN indexes on the tsvector columns using `CREATE INDEX ... USING gin(...)`.
- The migration must be idempotent — use `IF NOT EXISTS` for index creation.
- Reference the SeaORM migration pattern: implement `MigrationTrait` with `up` and `down` methods using raw SQL statements via `manager.get_connection().execute_unprepared(...)`.
- Per docs/constraints.md section 5 (Code Change Rules): changes must be scoped to files listed; code must not be modified without first inspecting it.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration demonstrating the SeaORM migration pattern, table creation, and index management in this project
- `common/src/db/query.rs` — shared query builder helpers that will consume these indexes in subsequent tasks

## Acceptance Criteria
- [ ] Migration adds tsvector generated columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] Migration runs successfully against a clean database
- [ ] Migration `down` method correctly removes the indexes and columns
- [ ] Existing queries and endpoints continue to work unchanged

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (no errors)
- [ ] Migration rollback (`down`) executes without errors
- [ ] Existing integration tests in `tests/api/` continue to pass after migration

## Verification Commands
- `cargo test --test api` — all existing integration tests pass
