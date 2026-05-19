## Repository
trustify-backend

## Target Branch
main

## Description
Add PostgreSQL full-text search infrastructure to support faster and more relevant search queries. This task creates a database migration that adds tsvector columns to searchable entities (sbom, advisory, package) and creates GIN indexes on those columns. It also adds a trigger-based tsvector update mechanism so the tsvector columns stay in sync with the source text columns. This is the foundational task -- subsequent tasks build on these indexes to deliver relevance ranking and filtering.

**Assumption (pending clarification -- see A1, A4 in impact map):** All three entity types (SBOM, advisory, package) are in scope for search improvements. The performance target is not yet quantified; this task provides the indexing infrastructure that enables measurable performance gains.

## Files to Modify
- `entity/src/sbom.rs` -- Add tsvector column to the SBOM SeaORM entity definition
- `entity/src/advisory.rs` -- Add tsvector column to the Advisory SeaORM entity definition
- `entity/src/package.rs` -- Add tsvector column to the Package SeaORM entity definition
- `common/src/db/query.rs` -- Add full-text search query builder helper functions (ts_query construction, ts_rank scoring)

## Files to Create
- `migration/src/m0002_fulltext_search/mod.rs` -- Migration that adds tsvector columns, GIN indexes, and trigger functions to sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for structure and naming conventions
- Register the new migration module in `migration/src/lib.rs`
- Use PostgreSQL `tsvector` type with `to_tsvector('english', ...)` for text processing
- Create GIN indexes on each tsvector column for fast full-text lookups: `CREATE INDEX idx_sbom_search ON sbom USING GIN (search_vector)`
- Add database triggers (`tsvector_update_trigger` or custom trigger functions) to automatically update tsvector columns when source text fields change
- For SBOMs: build tsvector from name and other descriptive fields
- For advisories: build tsvector from title, description, and severity-related text
- For packages: build tsvector from name, namespace/purl, and license text
- In `common/src/db/query.rs`, add helper functions alongside the existing filtering/pagination/sorting helpers. Follow the same module patterns (public functions, consistent error handling with `AppError`)
- The query helpers should provide: (1) a function to build a `tsquery` from user input (handling special characters and boolean operators), (2) a function to apply `ts_rank` scoring to a query
- Backfill existing rows by running an UPDATE in the migration to populate tsvector columns for pre-existing data

## Reuse Candidates
- `common/src/db/query.rs` -- Existing query builder helpers for filtering and pagination; add full-text search helpers alongside these
- `migration/src/m0001_initial/mod.rs` -- Migration structure and SeaORM migration patterns to follow
- `common/src/error.rs::AppError` -- Use for error handling in new query helpers

## Acceptance Criteria
- [ ] Migration creates tsvector columns on sbom, advisory, and package tables
- [ ] Migration creates GIN indexes on all tsvector columns
- [ ] Migration includes triggers or functions to keep tsvector columns updated on INSERT and UPDATE
- [ ] Migration backfills tsvector columns for existing rows
- [ ] SeaORM entity definitions in `entity/src/` include the new tsvector columns
- [ ] Query helper functions for tsquery construction and ts_rank scoring are added to `common/src/db/query.rs`
- [ ] Migration runs successfully against a clean database and against a database with existing data
- [ ] Existing tests in `tests/api/` continue to pass (no regressions)

## Test Requirements
- [ ] Migration up/down test: verify the migration applies and rolls back cleanly
- [ ] Integration test: insert a record, verify the tsvector column is populated by the trigger
- [ ] Integration test: update a record's text fields, verify the tsvector column is updated

## Verification Commands
- `cargo test --test api` -- all existing integration tests pass
- `cargo run --bin migration -- up` -- migration applies without errors

## Dependencies
- Depends on: None
