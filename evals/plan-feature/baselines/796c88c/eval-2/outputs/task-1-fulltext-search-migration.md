# Task 1: Database Migration for Full-Text Search Indexes

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds PostgreSQL full-text search infrastructure to support the "Improve search experience" feature (TC-9002). This migration adds `tsvector` columns and GIN indexes to the SBOM, advisory, and package tables, enabling efficient full-text search with relevance ranking.

This task addresses the "search should be faster" requirement by replacing implicit LIKE/ILIKE queries with GIN-indexed full-text search, which provides orders-of-magnitude better performance for text matching on large datasets.

**Ambiguity: "Search should be faster"** — The feature provides no baseline metrics or target latency. This migration assumes that switching from sequential scan text matching to GIN-indexed tsvector search is the intended improvement. If specific latency targets exist, they should be defined before this work is considered complete.

**Assumption (A1)**: The fields to index are SBOM name/description, advisory title/description, and package name/description. This assumption is pending clarification from the product owner on which fields users actually search.

## Files to Create
- `migration/src/m0002_fulltext_search/mod.rs` — Migration that adds tsvector columns, GIN indexes, and trigger functions for automatic tsvector updates on insert/update

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module `m0002_fulltext_search`
- `entity/src/sbom.rs` — Add `search_vector` column mapping (tsvector type) to the SBOM SeaORM entity
- `entity/src/advisory.rs` — Add `search_vector` column mapping to the Advisory SeaORM entity
- `entity/src/package.rs` — Add `search_vector` column mapping to the Package SeaORM entity

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and registration
- The migration should use raw SQL for PostgreSQL-specific features (tsvector, GIN index, trigger functions) since SeaORM migrations support `manager.get_connection().execute_unprepared()`
- Create a trigger function per table that automatically updates the tsvector column using `to_tsvector('english', coalesce(field1, '') || ' ' || coalesce(field2, ''))` on INSERT and UPDATE
- GIN indexes should be created with `CREATE INDEX idx_<table>_search ON <table> USING GIN(search_vector)`
- Entity column mappings in `entity/src/` follow the SeaORM `DeriveEntityModel` pattern — add the column as `Option<String>` since tsvector is managed by database triggers, not application code
- The `common/src/db/query.rs` module contains shared query helpers — full-text query support will be added in Task 2

**Assumption (A3)**: PostgreSQL built-in full-text search is sufficient. If the product owner requires features like fuzzy matching, typo tolerance, or faceted search, an external engine (Elasticsearch, Meilisearch) would be needed instead, which would significantly change this approach.

## Acceptance Criteria
- [ ] Migration creates `search_vector` tsvector columns on sbom, advisory, and package tables
- [ ] Migration creates GIN indexes on all `search_vector` columns
- [ ] Migration creates trigger functions that auto-populate tsvector on insert and update
- [ ] Migration includes a backfill step that populates tsvector for existing rows
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against a database with existing data (upgrade path)
- [ ] SeaORM entity definitions compile with the new column mappings

## Test Requirements
- [ ] Migration up/down works correctly (run migration, verify columns/indexes exist, run rollback, verify removed)
- [ ] Trigger function correctly populates tsvector on row insert
- [ ] Trigger function correctly updates tsvector on row update
- [ ] GIN index is used by query planner (EXPLAIN ANALYZE confirms index scan)

## Dependencies
- None — this is the foundational task

## Conventions

- **Module pattern**: Applies: task modifies `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` matching the convention's SeaORM entity scope.
