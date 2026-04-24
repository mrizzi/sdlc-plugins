# Task 1 — Add Database Migration for Search Indexes and Full-Text Search Support

## Repository
trustify-backend

## Description
Create a new database migration that adds PostgreSQL full-text search infrastructure and performance indexes to support faster, relevance-ranked search. This migration adds a `tsvector` column to key entities (sbom, advisory, package) for full-text search, creates GIN indexes on those columns, and adds B-tree indexes on commonly filtered columns (severity, license, timestamps). This is the foundational task that enables all subsequent search improvements.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that adds `tsvector` columns, GIN indexes for full-text search, B-tree indexes on filter columns, and a trigger to keep `tsvector` columns updated on INSERT/UPDATE

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation
- Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
- Create GIN indexes on each `search_vector` column for fast full-text search: `CREATE INDEX idx_sbom_search ON sbom USING GIN(search_vector)`
- Create B-tree indexes on commonly filtered columns:
  - `advisory.severity` for severity filtering
  - `package_license.license` for license filtering
  - `sbom.created_at` / `advisory.created_at` for date range filtering (if timestamp columns exist)
- Add a PostgreSQL trigger function that auto-populates the `search_vector` column using `to_tsvector('english', coalesce(name,'') || ' ' || coalesce(description,''))` on INSERT and UPDATE
- Per constraints doc section 2 (Commit Rules): commit must reference TC-9002 in the footer and follow Conventional Commits format
- Per constraints doc section 5.2: inspect the existing migration code in `migration/src/m0001_initial/mod.rs` before writing the new migration to follow the established patterns

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration pattern for SeaORM migration trait implementation and table alteration syntax

## Acceptance Criteria
- [ ] New migration module is registered in `migration/src/lib.rs`
- [ ] Migration adds `search_vector` tsvector columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] B-tree indexes are created on severity, license, and timestamp columns
- [ ] Trigger function auto-populates `search_vector` on INSERT and UPDATE
- [ ] Migration runs successfully against a clean database and against an existing database (up migration)
- [ ] Migration can be rolled back cleanly (down migration)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration applies cleanly on a database with existing data (backfill populates search_vector for existing rows)
- [ ] Down migration removes all created indexes, triggers, and columns without errors

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors
