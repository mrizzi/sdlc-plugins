# Task 1 — Add database indexes for search performance

## Repository
trustify-backend

## Description
Add database indexes to improve the performance of search queries. The existing
search module (`modules/search/`) queries across SBOM, advisory, and package entities
but the feature description provides no performance baseline or targets. This task
adds GIN indexes for full-text search columns to reduce query scan times.

**Ambiguity note:** The specific indexes needed depend on the current query patterns
in `SearchService` (`modules/search/src/service/mod.rs`) and the actual performance
bottlenecks. Without profiling data or latency targets ("should be faster" is the
only requirement), this task assumes PostgreSQL GIN indexes on text-searchable columns
are the appropriate optimization. The implementer should profile before and after to
validate the improvement, even though no target threshold is defined.

## Files to Modify
- `modules/search/src/service/mod.rs` — Review current query patterns to determine which columns need indexing

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration adding GIN indexes for full-text search columns on relevant entity tables

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`
- Per CONVENTIONS.md: database migrations use SeaORM migration pattern; see `migration/src/m0001_initial/mod.rs` for the established structure
- Use `Index::create()` for adding GIN indexes suitable for `tsvector` columns
- Review `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify text columns used in search queries
- The query builder helpers in `common/src/db/query.rs` may need awareness of new indexes for query planning, but do not modify query.rs in this task
- **Ambiguity:** Without knowing the current query execution plans, the specific columns to index are an educated guess. The implementer should run `EXPLAIN ANALYZE` on the current search queries before deciding which indexes to add

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers; inspect to understand current query patterns and filtering logic
- `migration/src/m0001_initial/mod.rs` — Migration pattern to follow for the new migration file

## Acceptance Criteria
- [ ] New database migration creates GIN indexes on text-searchable columns used by the search service
- [ ] Migration runs successfully against a fresh database and as an upgrade from the existing schema
- [ ] Existing search functionality is not broken (existing integration tests in `tests/api/search.rs` continue to pass)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (tested via migration runner)
- [ ] Migration applies cleanly as an upgrade on an existing database
- [ ] Existing `tests/api/search.rs` integration tests pass without modification

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test --test search` — existing search integration tests pass
