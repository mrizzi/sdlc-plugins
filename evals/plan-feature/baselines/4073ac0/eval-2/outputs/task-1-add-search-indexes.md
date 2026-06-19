## Repository
trustify-backend

## Target Branch
main

## Description
Add database migration to create full-text search indexes on searchable columns
across SBOM, advisory, and package entities. This addresses the "search should be
faster" requirement from TC-9002 by ensuring PostgreSQL can use GIN indexes for
full-text search queries instead of sequential scans.

ASSUMPTION (pending clarification): The performance issue is database query execution
time, and adding GIN indexes on text columns used by the search service will
materially improve query latency.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module that creates GIN indexes on searchable text columns in the sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_indexes migration module in the migration runner

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`.
The new migration should use SeaORM's migration trait (`MigrationTrait`) with an `up`
method that creates GIN indexes using `CREATE INDEX ... USING gin(to_tsvector(...))` raw
SQL statements, and a `down` method that drops them.

The entities that need indexes are defined in:
- `entity/src/sbom.rs` — SBOM entity (index name/description text fields)
- `entity/src/advisory.rs` — Advisory entity (index title/description text fields)
- `entity/src/package.rs` — Package entity (index name/purl text fields)

Register the new migration in `migration/src/lib.rs` following the pattern used for
`m0001_initial`.

Per CONVENTIONS.md §Module pattern: each domain module follows `model/ + service/ + endpoints/` structure.
Applies: convention has no file-type restriction (broadly applicable).

## Acceptance Criteria
- [ ] New migration creates GIN indexes on text columns used for full-text search in sbom, advisory, and package tables
- [ ] Migration includes a `down` method that cleanly drops the created indexes
- [ ] Migration is registered in `migration/src/lib.rs` and runs successfully
- [ ] Existing migrations continue to run without errors

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration rolls back cleanly (down method)
- [ ] Existing integration tests in `tests/api/` continue to pass after migration

## Dependencies
- Depends on: None — this is the first task in the sequence
