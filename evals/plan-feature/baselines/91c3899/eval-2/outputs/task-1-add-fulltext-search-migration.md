## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration to create full-text search infrastructure on SBOM, advisory, and package tables. This migration adds `tsvector` columns and GIN indexes to enable PostgreSQL native full-text search, replacing the current text matching approach with ranked, weighted search.

**ASSUMPTION pending clarification:** The specific fields to index are assumed based on the existing entity structure: SBOM name/description, advisory title/description/severity, and package name/license. The product owner should confirm which fields users consider most important for search.

## Files to Create
- `migration/src/m0002_fulltext_search_indexes/mod.rs` — Migration module that adds `search_vector` tsvector columns and GIN indexes to `sbom`, `advisory`, and `package` tables, plus trigger functions to keep tsvector columns updated on insert/update

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module `m0002_fulltext_search_indexes`

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and registration
- Use SeaORM migration framework — the migration should implement `MigrationTrait` with `up` and `down` methods
- Add `search_vector tsvector` column to each target table (`sbom`, `advisory`, `package`)
- Create GIN indexes on each `search_vector` column for fast full-text lookups
- Create trigger functions (`tsvector_update_trigger`) that automatically populate `search_vector` on INSERT/UPDATE using weighted concatenation of relevant fields:
  - `sbom`: weight A for name, weight B for description fields
  - `advisory`: weight A for title, weight B for description, weight C for severity
  - `package`: weight A for name, weight B for license
- Include a backfill statement in the `up` migration to populate `search_vector` for existing rows
- Per Key Conventions §Framework: use SeaORM for database operations. Applies: task modifies `migration/src/m0002_fulltext_search_indexes/mod.rs` matching the convention's SeaORM migration scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration pattern to follow for structure, registration, and SeaORM migration trait implementation

## Acceptance Criteria
- [ ] Migration adds `search_vector` tsvector column to `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on each `search_vector` column
- [ ] Trigger functions automatically update `search_vector` on row insert/update
- [ ] Existing rows are backfilled with search vectors
- [ ] Migration is reversible (`down` method drops columns, indexes, and triggers)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration runs successfully against a clean database (up)
- [ ] Migration rolls back cleanly (down)
- [ ] After migration, inserting a new SBOM row populates the `search_vector` column automatically
- [ ] After migration, existing rows have populated `search_vector` values

## Verification Commands
- `cargo test -p migration` — migration compiles and any migration-specific tests pass
