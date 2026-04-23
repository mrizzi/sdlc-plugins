## Repository
trustify-backend

## Description
Add a database migration that creates full-text search indexes on the SBOM, advisory, and package tables. This is the foundational step for improving search performance — without proper indexes, PostgreSQL performs sequential scans on text fields, which is the most likely cause of the reported slowness.

**Assumption pending clarification**: The feature description does not specify which fields are slow or which tables lack indexes. We assume that the core searchable entities (SBOMs, advisories, packages) need GIN indexes on `tsvector` columns for full-text search. If the existing schema already has indexes, this migration adds the missing full-text-specific ones.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module that creates GIN indexes on tsvector columns for the sbom, advisory, and package tables. Also adds generated `tsvector` columns if they do not already exist.

## Files to Modify
- `migration/src/lib.rs` — Register the new `m0002_search_indexes` migration module in the migration runner's list of migrations.

## Implementation Notes
- Follow the pattern in `migration/src/m0001_initial/mod.rs` for migration structure. Each migration module implements SeaORM's `MigrationTrait` with `up()` and `down()` methods.
- Create `tsvector` columns using PostgreSQL's `to_tsvector('english', ...)` on relevant text fields (e.g., name, description for SBOMs; title, description for advisories; name, namespace for packages).
- Create GIN indexes on the new `tsvector` columns: `CREATE INDEX idx_sbom_fts ON sbom USING GIN(search_vector)` and similar for advisory and package tables.
- Reference `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the actual column names that should be included in the tsvector expressions.

## Acceptance Criteria
- [ ] Migration creates `tsvector` columns on sbom, advisory, and package tables
- [ ] Migration creates GIN indexes on all new `tsvector` columns
- [ ] Migration is reversible (`down()` drops the indexes and columns)
- [ ] Migration runs successfully against a fresh database and against a database with existing data
- [ ] The new migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies cleanly on an empty database (`cargo run --bin migration -- up`)
- [ ] Migration rolls back cleanly (`cargo run --bin migration -- down`)
- [ ] After migration, `\di` in psql shows the new GIN indexes on sbom, advisory, and package tables
- [ ] Existing data is preserved after migration (no data loss)

## Dependencies
- Depends on: None
