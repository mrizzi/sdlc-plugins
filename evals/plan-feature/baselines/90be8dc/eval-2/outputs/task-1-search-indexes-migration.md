## Repository
trustify-backend

## Description
Create a database migration to add PostgreSQL full-text search indexes (GIN indexes on `tsvector` columns) to the SBOM, advisory, and package tables. This is the foundation for improving search performance and enabling relevance ranking. Without proper indexes, full-text search queries perform sequential scans, which is the most likely cause of the "search is slow" complaints.

**Assumption pending clarification:** We assume PostgreSQL full-text search (tsvector/tsquery with GIN indexes) is the appropriate solution rather than an external search engine like Elasticsearch. This should be confirmed with the team.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Database migration that adds `search_vector` tsvector columns and GIN indexes to `sbom`, `advisory`, and `package` tables, plus triggers to keep vectors updated on insert/update

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module `m0002_search_indexes`

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`. The migration should:

1. Add a `search_vector tsvector` column to each table (`sbom`, `advisory`, `package`) defined in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`.
2. Create GIN indexes on these columns: `CREATE INDEX idx_sbom_search ON sbom USING GIN(search_vector)`.
3. Create trigger functions that populate `search_vector` from relevant text fields on INSERT and UPDATE.
4. Backfill existing rows by running an UPDATE to populate `search_vector` for all current data.
5. Use SeaORM migration patterns consistent with the project conventions in `CONVENTIONS.md`.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Reference for migration structure and SeaORM migration trait implementation

## Acceptance Criteria
- [ ] Migration adds `search_vector` tsvector column to `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Triggers auto-populate `search_vector` on insert and update
- [ ] Existing rows are backfilled with search vectors
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration runs successfully against a clean database and as an upgrade from `m0001_initial`

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration applies cleanly as an upgrade from the initial migration
- [ ] Rollback/down migration drops the indexes, triggers, and columns without errors
- [ ] After migration, inserting a new SBOM row populates `search_vector` automatically

## Verification Commands
- `cargo run -p migration -- up` — Migration applies without errors
- `cargo run -p migration -- down` — Rollback completes without errors
