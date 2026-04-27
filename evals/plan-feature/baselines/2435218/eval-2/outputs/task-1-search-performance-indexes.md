# Task 1 — Add database indexes for search performance

**Feature:** TC-9002 — Improve search experience
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Description
Add database indexes to improve full-text search query performance. The current search implementation in `SearchService` performs full-text search across SBOMs, advisories, and packages but lacks dedicated indexes for text search fields. This task adds GIN/GiST indexes on searchable text columns (names, descriptions, identifiers) to reduce query latency.

**Ambiguity flag:** The feature does not specify a target latency. This task assumes the goal is to bring p95 search response time below 500ms. The actual performance target should be confirmed with the product owner. A baseline measurement should be taken before and after index creation.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New SeaORM migration adding GIN indexes on searchable text columns across SBOM, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`
- Use PostgreSQL GIN indexes with `pg_trgm` extension for trigram-based text search, or `to_tsvector`/`to_tsquery` for full-text search — inspect the current `SearchService` implementation in `modules/search/src/service/mod.rs` to determine which approach the existing search uses, then add indexes that match
- The existing query builder helpers in `common/src/db/query.rs` handle filtering and pagination — indexes should be designed to support the query patterns used there
- Per docs/constraints.md Section 2 (Commit Rules): commit must reference TC-9002 in the footer, use Conventional Commits format, and include `--trailer="Assisted-by: Claude Code"`
- Per docs/constraints.md Section 3 (PR Rules): branch must be named after the Jira issue ID

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Existing migration pattern showing SeaORM migration structure, table creation, and index creation conventions
- `common/src/db/query.rs` — Shared query builder helpers; inspect to understand current query patterns that indexes should optimize

## Acceptance Criteria
- [ ] A new database migration creates GIN or appropriate text search indexes on searchable columns in SBOM, advisory, and package tables
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration applies cleanly on a database with existing data (upgrade path)
- [ ] Verify index existence via SQL query after migration runs
- [ ] Existing search integration tests pass without modification

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test -p tests --test search` — existing search tests pass

## Dependencies
- None (this is a foundational task)
