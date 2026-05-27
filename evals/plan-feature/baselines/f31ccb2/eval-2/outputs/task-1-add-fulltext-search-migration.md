## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration to create PostgreSQL full-text search infrastructure. This migration adds `tsvector` columns to the `sbom`, `advisory`, and `package` tables for full-text indexing, creates GIN indexes on those columns, and adds a trigger to keep the tsvector columns updated automatically. This is the foundational change that enables relevance-ranked full-text search in subsequent tasks.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_fulltext_search/mod.rs` — migration that adds tsvector columns, GIN indexes, and update triggers to sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` — use SeaORM migration traits (`MigrationTrait`, `SchemaManager`)
- Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
- Create GIN indexes on each `search_vector` column for fast full-text lookups: `CREATE INDEX idx_sbom_search_vector ON sbom USING GIN(search_vector)`
- Add trigger functions using `tsvector_update_trigger` or a custom PL/pgSQL function to populate the tsvector column on INSERT and UPDATE
- Include a data migration step that populates the tsvector column for existing rows
- Use weighted tsvector concatenation (setweight) to prioritize name/title fields ('A') over description fields ('B')

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — established migration pattern for table creation and schema changes

## Acceptance Criteria
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing data (backfill)
- [ ] `sbom`, `advisory`, and `package` tables each have a `search_vector` tsvector column
- [ ] GIN indexes exist on all three `search_vector` columns
- [ ] Inserting or updating a row automatically updates the `search_vector` column

## Test Requirements
- [ ] Migration up and down both execute without errors
- [ ] Verify tsvector columns are populated correctly after migration on existing data
- [ ] Verify GIN indexes are created by querying `pg_indexes`

## Dependencies
- None
