# Task 1 — Add Full-Text Search Indexes via Database Migration

## Repository
trustify-backend

## Description
Create a new SeaORM database migration that adds PostgreSQL GIN indexes for full-text search on searchable entity columns. This addresses the "search should be faster" requirement by enabling PostgreSQL to use inverted indexes for text search instead of sequential scans. The migration adds `tsvector` columns and GIN indexes on the SBOM, advisory, and package tables to support efficient full-text search queries.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration that adds `tsvector` columns and GIN indexes on `sbom`, `advisory`, and `package` tables for full-text search

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and naming conventions.
- Use SeaORM's migration API to create the `tsvector` columns and GIN indexes. The `tsvector` columns should be populated via a trigger or a generated column expression combining the searchable text fields for each entity.
- For the `sbom` table: index on name/title fields. For `advisory`: index on title, description, severity. For `package`: index on name, namespace, license.
- Use `Index::create().table(...).name(...).col(...).index_type(IndexType::Gin)` pattern for creating GIN indexes.
- Refer to `common/src/db/query.rs` for understanding how existing queries interact with these tables — the new indexes must be compatible with the query patterns used there.
- Per `docs/constraints.md` section 2 (Commit Rules): commit must reference TC-9002 in the footer and follow Conventional Commits format.
- Per `docs/constraints.md` section 5 (Code Change Rules): inspect existing migration code before writing new migration.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern to follow for structure, naming, and SeaORM migration API usage
- `common/src/db/query.rs` — shared query builder helpers that will consume these indexes; review to ensure index compatibility

## Acceptance Criteria
- [ ] New migration module is registered in `migration/src/lib.rs`
- [ ] Migration creates `tsvector` columns on `sbom`, `advisory`, and `package` tables
- [ ] Migration creates GIN indexes on the new `tsvector` columns
- [ ] Migration is reversible (implements `down` method to drop indexes and columns)
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing data (backfill of `tsvector` columns)

## Test Requirements
- [ ] Migration applies cleanly on an empty database (`cargo run --bin migration -- up`)
- [ ] Migration rolls back cleanly (`cargo run --bin migration -- down`)
- [ ] After migration, `tsvector` columns are populated for existing rows
- [ ] GIN indexes are visible in the PostgreSQL catalog (`pg_indexes`)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors
