# Task 1 — Add Full-Text Search Indexes via Database Migration

## Repository
trustify-backend

## Description
Create a database migration that adds PostgreSQL full-text search indexes (using `tsvector` columns and GIN indexes) on the primary searchable columns across SBOM, advisory, and package entities. This is the foundational change that enables both improved search performance and relevance ranking in subsequent tasks.

Currently the search service likely performs unoptimized `LIKE` or `ILIKE` queries against raw text columns, which degrades performance as data volume grows. Adding dedicated `tsvector` columns with GIN indexes enables PostgreSQL's built-in full-text search with efficient index lookups and native relevance ranking via `ts_rank`.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration that adds `tsvector` columns and GIN indexes on searchable fields: SBOM name, advisory title, advisory severity, package name, and package license

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- Use PostgreSQL `tsvector` columns with `GIN` indexes for full-text search. Each searchable entity table should get a generated `tsvector` column that concatenates the relevant text fields with appropriate weights (e.g., `setweight(to_tsvector('english', name), 'A')` for primary fields, weight 'B' for secondary fields).
- Add a trigger or generated column to keep the `tsvector` column in sync with source columns on INSERT/UPDATE.
- Per the repo conventions: the framework uses SeaORM for database access. Use SeaORM's raw SQL migration support for PostgreSQL-specific DDL (tsvector, GIN index creation).
- Per constraints doc section 2 (Commit Rules): commit must reference TC-9002 in footer, use Conventional Commits format, include `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — reference for migration module structure, SeaORM migration trait implementation pattern
- `common/src/db/query.rs` — shared query builder helpers; review existing filtering patterns to ensure the new indexes align with how queries are constructed

## Acceptance Criteria
- [ ] A new migration module exists and is registered in `migration/src/lib.rs`
- [ ] The migration creates `tsvector` columns on SBOM, advisory, and package tables
- [ ] GIN indexes are created on all new `tsvector` columns
- [ ] The migration is reversible (includes a down/rollback implementation)
- [ ] The migration runs successfully against a clean PostgreSQL database

## Test Requirements
- [ ] Migration applies cleanly on an empty database (forward migration)
- [ ] Migration rolls back cleanly (reverse migration)
- [ ] After migration, `tsvector` columns are populated for existing rows (if any test seed data exists)
- [ ] GIN indexes are present and usable (verify via `\di` or `pg_indexes` query in test)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors
