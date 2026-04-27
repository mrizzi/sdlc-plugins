## Repository
trustify-backend

## Description
Add a PostgreSQL full-text search index migration to enable efficient full-text search across SBOM, advisory, and package entities. This migration creates `tsvector` columns and GIN indexes on the searchable fields of these entities, providing the database-level foundation for improved search relevance and performance.

**Ambiguity note:** The feature description does not specify which fields should be searchable. This task assumes the following fields based on the existing entity definitions (assumption pending clarification with product owner):
- SBOM: name, document identifier fields
- Advisory: title, description, severity
- Package: name, namespace, license

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that adds `tsvector` columns and GIN indexes for full-text search on SBOM, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. Each migration module defines `up` and `down` functions using SeaORM migration traits.
- The migration should:
  1. Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
  2. Create a GIN index on each `search_vector` column for fast full-text search
  3. Create a trigger function that automatically updates the `search_vector` column when rows are inserted or updated, concatenating the relevant text fields with appropriate weights (e.g., `setweight(to_tsvector('english', coalesce(name, '')), 'A')`)
- Register the migration in `migration/src/lib.rs` by adding it to the migration list, following the pattern of how `m0001_initial` is registered.
- Per the Key Conventions: use SeaORM for database operations. The migration crate has its own `Cargo.toml` at `migration/Cargo.toml`.
- **Ambiguity note:** Field weights (A, B, C, D) for `tsvector` are assumed as follows: entity name/title fields get weight A (highest), description fields get weight B, and identifier/metadata fields get weight C. These weights affect search ranking in Task 2. Confirm with product owner.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern to follow for structure, up/down functions, and SeaORM migration trait usage

## Acceptance Criteria
- [ ] A new migration module `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] Running the migration adds `search_vector` tsvector columns to `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Trigger functions are created to auto-populate `search_vector` on insert and update
- [ ] The `down` migration cleanly removes all added columns, indexes, and triggers
- [ ] Existing data is backfilled by running an initial UPDATE to populate `search_vector` for existing rows

## Test Requirements
- [ ] Migration runs successfully against a clean PostgreSQL test database
- [ ] Migration `down` function successfully rolls back all changes
- [ ] After migration, inserting a row into `sbom`, `advisory`, or `package` tables auto-populates the `search_vector` column
- [ ] GIN indexes are verified to exist via `pg_indexes` system catalog query
