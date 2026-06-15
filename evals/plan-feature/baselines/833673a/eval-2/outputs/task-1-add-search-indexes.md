## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes on text columns used by the search service to improve query performance. The current search implementation in `modules/search/src/service/mod.rs` queries across SBOM, advisory, and package entities without dedicated indexes on the searched text fields. This task creates a new SeaORM migration that adds B-tree indexes on commonly searched columns and a GIN index on a `tsvector` column to support full-text search in subsequent tasks.

**Assumptions pending clarification:**
- The specific columns to index are assumed to be entity name/title and description fields on the `sbom`, `advisory`, and `package` tables. The feature description does not specify which fields are "slow" — this assumption is based on the entity model structures in `entity/src/`.
- The target performance improvement is assumed to be measurable via `EXPLAIN ANALYZE` showing index scans replacing sequential scans. No quantitative latency target was provided in the feature requirements.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration adding B-tree and GIN indexes on searchable text columns across sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner
- `entity/src/sbom.rs` — Add `tsvector` column to the SBOM entity for full-text search support
- `entity/src/advisory.rs` — Add `tsvector` column to the advisory entity for full-text search support
- `entity/src/package.rs` — Add `tsvector` column to the package entity for full-text search support

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and registration.
- Use SeaORM's migration API (`Index::create()`) to define the indexes, consistent with the project's ORM-based migration approach.
- Add a `tsvector` generated column on each entity table that concatenates the searchable text fields (e.g., name, description) using `to_tsvector('english', ...)`. This column will be used by the full-text search implementation in Task 2.
- Create a GIN index on each `tsvector` column for efficient full-text search.
- Add standard B-tree indexes on individual name/title columns for exact-match and prefix queries.
- Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the correct column names.

## Reuse Candidates
- `common/src/db/query.rs::filtering/pagination helpers` — Existing query builder helpers that may need to be aware of new indexed columns for query planning
- `migration/src/m0001_initial/mod.rs` — Reference migration demonstrating the project's SeaORM migration pattern and conventions

## Acceptance Criteria
- [ ] A new migration exists that adds B-tree indexes on searchable text columns (name/title, description) for sbom, advisory, and package tables
- [ ] A GIN index is created on a `tsvector` generated column for each entity table
- [ ] The migration runs successfully against a clean database and is idempotent
- [ ] Entity definitions are updated with the `tsvector` column
- [ ] Existing integration tests in `tests/api/` continue to pass without modification

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (verified via migration runner)
- [ ] Migration applies cleanly on an existing database with data (upgrade path)
- [ ] `EXPLAIN ANALYZE` on a basic search query shows index usage instead of sequential scan
- [ ] All existing tests in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` pass without changes

## Verification Commands
- `cargo test --test api` — all existing API integration tests pass

[sdlc-workflow] Description digest: sha256-md:1b3f2569da3318a8c276664b22a7f6b1ef7560a83b03083c469724d786257140
