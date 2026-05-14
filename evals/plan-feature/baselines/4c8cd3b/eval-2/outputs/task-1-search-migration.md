## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates tsvector columns and GIN indexes on the SBOM, advisory, and package tables to support full-text search with relevance ranking. This migration is the foundation for all subsequent search improvements in TC-9002 -- without these indexes, full-text search queries would require sequential scans.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- Migration module that adds tsvector columns and GIN indexes to the sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` -- Register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` -- use SeaORM's migration trait with `up` and `down` methods.
- For each entity table (sbom, advisory, package), add:
  - A `search_vector` column of type `tsvector` that is populated via a trigger or generated column combining the relevant searchable text fields.
  - A GIN index on the `search_vector` column for fast full-text search lookups.
- For the SBOM table (`entity/src/sbom.rs`): combine name and description fields into the tsvector.
- For the advisory table (`entity/src/advisory.rs`): combine title, description, and severity fields into the tsvector. Weight the title field higher (setweight 'A') than description (setweight 'B').
- For the package table (`entity/src/package.rs`): combine name and license fields into the tsvector.
- Use `CREATE INDEX ... USING GIN (search_vector)` for the index creation.
- Add a database trigger (`tsvector_update_trigger` or a PostgreSQL generated column) to keep the `search_vector` column in sync with source columns on INSERT and UPDATE.
- The `down` method must drop the indexes and columns in reverse order.
- Per constraints doc section 2 (Commit Rules): commit must reference TC-9002 in the footer and follow Conventional Commits format.

## Acceptance Criteria
- [ ] Migration creates tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on each tsvector column
- [ ] Triggers or generated columns keep tsvector columns in sync with source text fields
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration `down` method reverses all changes cleanly
- [ ] Existing data is not lost or corrupted by the migration

## Test Requirements
- [ ] Migration runs successfully against a clean database (up)
- [ ] Migration rolls back successfully (down)
- [ ] After migration, inserting a row into each table populates the search_vector column automatically
- [ ] GIN indexes are verified to exist via a database metadata query

## Verification Commands
- `cargo test -p migration` -- migration tests pass
