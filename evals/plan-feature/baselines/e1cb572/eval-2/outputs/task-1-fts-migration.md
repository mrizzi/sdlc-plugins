# Task 1: Add Database Migration for Full-Text Search Indexes

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new SeaORM migration that adds PostgreSQL `tsvector` columns and GIN indexes to the `sbom`, `advisory`, and `package` tables. These columns will store pre-computed full-text search vectors, and the GIN indexes will enable fast full-text search queries. This is the foundational data layer change required before the search service can be updated to use PostgreSQL full-text search.

**Ambiguity note:** The feature description does not specify which fields should be searchable per entity. This task assumes the following fields are indexed for search (pending product owner clarification):
- SBOM: name, document identifier
- Advisory: title, description, severity
- Package: name, namespace/vendor

## Files to Create
- `migration/src/m0002_fts_indexes/mod.rs` — New migration module that adds `search_vector` (`tsvector`) columns and GIN indexes to `sbom`, `advisory`, and `package` tables, plus triggers to auto-update vectors on insert/update

## Files to Modify
- `migration/src/lib.rs` — Register the new `m0002_fts_indexes` migration module in the migration list

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and conventions.
- Use SeaORM's `manager.exec_stmt()` or raw SQL via `manager.get_connection().execute_unprepared()` to create the `tsvector` columns, GIN indexes, and update triggers.
- The migration should:
  1. Add a `search_vector tsvector` column to each table (sbom, advisory, package)
  2. Create a GIN index on each `search_vector` column for fast lookups
  3. Create a trigger function that auto-populates `search_vector` using `to_tsvector('english', ...)` on the relevant text columns
  4. Backfill existing rows by running an UPDATE to populate `search_vector` for current data
- Per CONVENTIONS.md: use SeaORM migration patterns.
  Applies: task modifies `migration/src/m0002_fts_indexes/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration for structural reference on how migrations are organized in this project

## Acceptance Criteria
- [ ] Migration runs successfully against a PostgreSQL database
- [ ] `sbom`, `advisory`, and `package` tables each have a `search_vector` column of type `tsvector`
- [ ] GIN indexes exist on all three `search_vector` columns
- [ ] Triggers auto-update `search_vector` on INSERT and UPDATE
- [ ] Existing rows are backfilled with search vector data
- [ ] Migration is reversible (down migration drops columns, indexes, and triggers)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (up)
- [ ] Migration rolls back cleanly (down)
- [ ] After migration, inserting a new row auto-populates the `search_vector` column

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors

---

`[sdlc-workflow] Description digest: sha256-md:a3f1c7e9d4b82a6f0e5c93d17b24f68a0d9e3c5b7f1a284d6e09c3b5f7a81d2e`
