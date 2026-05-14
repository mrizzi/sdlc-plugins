# Task 1 — Add full-text search indexes migration

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds full-text search indexes (GIN indexes on `tsvector` columns) to the searchable entity tables: SBOM (name), advisory (title, description), and package (name). This migration lays the groundwork for the ranked search and filter features by enabling PostgreSQL full-text search capabilities on the relevant columns.

**Ambiguity note:** The feature description does not specify which fields should be searchable. This task assumes the most commonly queried text fields based on the existing entity model: SBOM name, advisory title and description, and package name. If additional fields should be searchable, this migration can be extended in a follow-up task.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that adds GIN indexes for full-text search on SBOM name, advisory title/description, and package name columns

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and naming conventions.
- Use PostgreSQL `tsvector` and GIN index types for full-text search support. The migration should add `tsvector` generated columns (or use `to_tsvector` in the index definition) for the target text columns.
- The migration module must be registered in `migration/src/lib.rs` following the pattern used for `m0001_initial`.
- Use SeaORM migration traits consistent with the existing migration infrastructure.
- Ensure the migration is idempotent — use `IF NOT EXISTS` guards where applicable.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration pattern to follow for module structure, trait implementations, and SeaORM migration conventions

## Acceptance Criteria
- [ ] A new migration module exists at `migration/src/m0002_search_indexes/mod.rs`
- [ ] The migration creates GIN indexes for full-text search on: SBOM name, advisory title, advisory description, and package name
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] The migration runs successfully against a PostgreSQL test database without errors
- [ ] The migration is reversible (implements both `up` and `down`)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (after m0001_initial)
- [ ] Migration rolls back cleanly without leaving artifacts
- [ ] Indexes are verified to exist after migration via database introspection

## Dependencies
- None
