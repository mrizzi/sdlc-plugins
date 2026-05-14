# Task 1 — Add full-text search database migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a SeaORM database migration that adds PostgreSQL full-text search infrastructure to the sbom, advisory, and package tables. This adds `tsvector` columns with GIN indexes to enable efficient full-text search with relevance ranking, replacing the current pattern-matching approach in the `SearchService`.

This is the foundational task — subsequent tasks depend on these indexes existing in the database schema.

**Assumption pending clarification:** The specific columns indexed are assumed based on likely search targets: name/description for SBOMs, title/description for advisories, and name for packages. Confirm with product owner which fields users actually search by.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_full_text_search/mod.rs` — migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration conventions.
- The migration should:
  1. Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables.
  2. Create GIN indexes on each `search_vector` column for fast full-text search.
  3. Create trigger functions to automatically update `search_vector` when rows are inserted or updated.
  4. Populate `search_vector` for existing rows using `to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))` (adjust columns per entity).
- For advisory entities, include the severity field in the tsvector so users can find advisories by severity text.
- Use `sea_orm_migration::prelude::*` and raw SQL via `manager.get_connection().execute_unprepared()` for PostgreSQL-specific DDL (tsvector, GIN indexes, trigger functions).
- Per `docs/constraints.md` section 2 (Commit Rules): commits must reference TC-9002 in the footer and follow Conventional Commits format.
- Per `docs/constraints.md` section 3 (PR Rules): branch must be named `TC-9002` or a sub-identifier.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern to follow for module structure, `MigrationTrait` implementation, and `up`/`down` methods
- `common/src/db/query.rs` — shared query builder helpers; review for any existing full-text search support before creating new infrastructure

## Acceptance Criteria
- [ ] A new migration module `m0002_full_text_search` exists and is registered in `migration/src/lib.rs`
- [ ] The migration adds `search_vector` (tsvector) columns to the sbom, advisory, and package tables
- [ ] GIN indexes are created on each `search_vector` column
- [ ] Trigger functions automatically update `search_vector` on INSERT and UPDATE
- [ ] The migration includes a `down` method that reverses all changes (drops triggers, indexes, and columns)
- [ ] Existing data is backfilled with tsvector values during migration

## Test Requirements
- [ ] The migration runs successfully against a clean database (up migration)
- [ ] The migration rolls back cleanly (down migration)
- [ ] After migration, inserting a row into sbom/advisory/package populates the `search_vector` column automatically via the trigger
- [ ] The GIN indexes are present and used by PostgreSQL for `@@` (full-text match) queries (verify with `EXPLAIN ANALYZE`)

## Verification Commands
- `cargo run --bin migration -- up` — migration completes without error
- `cargo run --bin migration -- down` — rollback completes without error
