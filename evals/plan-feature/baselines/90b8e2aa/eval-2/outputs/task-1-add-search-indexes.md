## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates GIN indexes on text-searchable columns across the SBOM, advisory, and package entities to improve full-text search query performance. The current search implementation in `modules/search/src/service/mod.rs` performs full-text search across multiple entity tables without dedicated text search indexes, resulting in sequential scans on large datasets.

This task addresses the "search should be faster" requirement from TC-9002. **Assumption (pending clarification):** the performance target is p95 latency under 500ms for search queries, as no specific threshold was provided in the feature description.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — database migration adding GIN indexes for full-text search on SBOM name/description, advisory title/description, and package name fields

## Files to Modify
- `migration/src/lib.rs` — register the new m0002_search_indexes migration module

## Implementation Notes
- Use SeaORM migration pattern to create GIN indexes (`CREATE INDEX ... USING gin(to_tsvector('english', column))`) on the text columns used by SearchService.
- Target columns based on the entity definitions in `entity/src/`:
  - `entity/src/sbom.rs` — SBOM name and description fields
  - `entity/src/advisory.rs` — advisory title and description fields
  - `entity/src/package.rs` — package name field
- Follow the existing migration structure in `migration/src/m0001_initial/mod.rs` for the migration module pattern.
- Per CONVENTIONS.md: use SeaORM migration API (`Index::create()`) for index creation statements. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.
- The migration must be idempotent — use `IF NOT EXISTS` where supported or handle the case where indexes already exist.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the SeaORM migration pattern (up/down methods, table/index creation)
- `entity/src/sbom.rs` — SBOM entity definition showing column names to index
- `entity/src/advisory.rs` — advisory entity definition showing column names to index
- `entity/src/package.rs` — package entity definition showing column names to index

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` exists and registers correctly in `migration/src/lib.rs`
- [ ] GIN indexes are created on text-searchable columns of SBOM, advisory, and package entities
- [ ] The migration runs successfully against a PostgreSQL database without errors
- [ ] The migration is reversible (down method drops the created indexes)
- [ ] Existing search functionality continues to work after the migration runs

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (up)
- [ ] Migration rolls back cleanly (down)
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass after migration

## Verification Commands
- `cargo test -p migration` — migration compiles and any migration-level tests pass
- `cargo test -p tests --test search` — existing search integration tests pass
