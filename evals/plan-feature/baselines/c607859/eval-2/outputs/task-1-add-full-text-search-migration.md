# Task 1 — Add Full-Text Search Migration

## Repository
trustify-backend

## Description
Create a new database migration that adds PostgreSQL full-text search indexes
to the `sbom`, `advisory`, and `package` tables. This is the foundational change
that enables the search performance and relevance improvements required by TC-9002.

The migration should add `tsvector` columns (or generated columns) to each
searchable table and create GIN indexes on them. This allows PostgreSQL's
built-in full-text search engine to be used for ranked retrieval instead of
naive `LIKE`/`ILIKE` queries.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_full_text_search/mod.rs` — migration that adds `tsvector`
  columns and GIN indexes for sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`.
  Use SeaORM's migration API (`sea_orm_migration::prelude::*`).
- For each table, add a generated `tsvector` column that concatenates the
  searchable text fields:
  - `sbom`: combine name/title and description fields
  - `advisory`: combine title, description, and severity fields
  - `package`: combine name and license fields
- Create a GIN index on each `tsvector` column for fast full-text lookups:
  `CREATE INDEX idx_sbom_fts ON sbom USING GIN(search_vector)`
- Use `to_tsvector('english', ...)` for the column generation to enable
  English stemming and stop-word removal.
- Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`,
  and `entity/src/package.rs` to identify the correct column names.
- Per constraints.md §2.1: commit must reference TC-9002 in the footer.
- Per constraints.md §5.1: changes must be scoped to the files listed above.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern showing
  SeaORM migration structure, table creation, and index creation
- `common/src/db/query.rs` — shared query builder helpers; review for any
  existing full-text search utilities before creating new ones

## Acceptance Criteria
- [ ] New migration module is registered in `migration/src/lib.rs`
- [ ] Migration creates `tsvector` generated columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all `tsvector` columns
- [ ] Migration runs successfully against a clean database (up)
- [ ] Migration rolls back cleanly (down)
- [ ] Existing data is populated in the `tsvector` columns after migration

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration rolls back without errors
- [ ] Verify GIN indexes exist after migration using `pg_indexes` query
- [ ] Verify `tsvector` columns are populated for existing rows

## Verification Commands
- `cargo run -p migration -- up` — migration applies successfully
- `cargo run -p migration -- down` — migration rolls back successfully

## Dependencies
- None (this is the foundational task)
