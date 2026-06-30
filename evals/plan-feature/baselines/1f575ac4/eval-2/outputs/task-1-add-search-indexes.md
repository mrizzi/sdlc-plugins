# Task 1 — Add database indexes for search-critical columns

**Summary:** Add database migration with full-text search indexes for SBOM, advisory, and package entities

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new database migration that adds GIN indexes for full-text search on the key text columns used by the search service. Currently, search queries against SBOM names, advisory titles/descriptions, and package names likely perform sequential scans. Adding tsvector GIN indexes enables PostgreSQL's full-text search engine to efficiently query these columns, directly addressing the "search is slow" feedback from users.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that adds GIN indexes on tsvector columns for `sbom` (name, document_id), `advisory` (title, description), and `package` (name) tables. Also adds a generated tsvector column to each table for efficient full-text search.

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` — examine its structure for the SeaORM migration trait implementation (`MigrationTrait`, `up`, `down` methods).
- The migration should create a `search_vector` column of type `tsvector` on each table (`sbom`, `advisory`, `package`) using a `GENERATED ALWAYS AS` expression that combines the relevant text columns with appropriate weights (e.g., name gets weight A, description gets weight B).
- Create GIN indexes on the generated `search_vector` columns using `CREATE INDEX ... USING gin(search_vector)`.
- The `down` method must drop the indexes and columns to ensure reversibility.
- Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the exact column names to index.
- Per the framework conventions, use SeaORM's `sea_query` for DDL operations within the migration.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Established migration pattern to follow for structure and SeaORM migration trait implementation.
- `entity/src/sbom.rs` — SBOM entity definition; confirms column names for index targets.
- `entity/src/advisory.rs` — Advisory entity definition; confirms column names for index targets.
- `entity/src/package.rs` — Package entity definition; confirms column names for index targets.

## Acceptance Criteria
- [ ] A new migration module exists and is registered in `migration/src/lib.rs`
- [ ] GIN indexes are created on full-text search vector columns for `sbom`, `advisory`, and `package` tables
- [ ] The migration is reversible (`down` method drops indexes and generated columns)
- [ ] The migration runs successfully against a PostgreSQL test database

## Test Requirements
- [ ] Migration applies cleanly to a fresh database (`cargo run --bin migration -- up`)
- [ ] Migration rolls back cleanly (`cargo run --bin migration -- down`)
- [ ] Verify GIN indexes exist after migration using `\di` or equivalent query

## Verification Commands
- `cargo run --bin migration -- up` — Migration applies without errors
- `cargo run --bin migration -- down` — Migration rolls back without errors

## Dependencies
- None (this is the foundational task)
