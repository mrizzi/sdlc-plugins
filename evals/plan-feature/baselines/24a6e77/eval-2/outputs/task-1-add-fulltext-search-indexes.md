# Task 1 — Add Full-Text Search Indexes via Database Migration

## Repository
trustify-backend

## Description
Create a new database migration that adds PostgreSQL GIN indexes for full-text search on searchable columns across SBOM, Advisory, and Package entities. This is the foundational performance improvement that enables weighted full-text search ranking in subsequent tasks. Without proper indexes, full-text search queries will perform sequential scans on large datasets, causing the slow search performance users have reported.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration adding GIN indexes on `tsvector` columns for `sbom`, `advisory`, and `package` tables

## Implementation Notes
- Follow the migration pattern established in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation
- Create `tsvector` generated columns (or use `to_tsvector()` in index expressions) for the following searchable fields:
  - `sbom` table: name/title fields
  - `advisory` table: title, description, severity fields
  - `package` table: name, license fields
- Use `CREATE INDEX ... USING GIN (to_tsvector('english', <column>))` for each searchable column
- Consider creating a composite `tsvector` column per entity that combines multiple fields with different weights (A, B, C, D) for ranked search — e.g., `setweight(to_tsvector('english', title), 'A') || setweight(to_tsvector('english', description), 'B')`
- Per constraints doc section 2: commit must reference TC-9002 in footer, use Conventional Commits format, include `--trailer="Assisted-by: Claude Code"`

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern to follow for module structure and SeaORM migration implementation

## Acceptance Criteria
- [ ] New migration module is registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on searchable columns for SBOM, Advisory, and Package entities
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Migration is reversible (implements `down()` to drop the indexes)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (run via `sea-orm-cli migrate up`)
- [ ] Migration rolls back cleanly (run via `sea-orm-cli migrate down`)
- [ ] Verify indexes exist after migration using `\di` or equivalent query against `pg_indexes`

## Verification Commands
- `cargo test -p migration` — migration compiles and any migration-level tests pass
