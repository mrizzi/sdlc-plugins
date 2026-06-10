# Task 1 — Optimize search query performance

## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query performance in the search module by adding database indexes for full-text search columns and improving the query execution plan. The feature description states search is "currently too slow" but provides no quantitative latency targets (**assumption pending clarification**: we target measurable improvement via indexing and query optimization, with benchmarks added so performance can be quantified post-implementation). This task addresses the "Search should be faster" MVP requirement from TC-9002.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize SearchService query construction to use indexed columns and reduce unnecessary joins
- `common/src/db/query.rs` — add or extend shared query builder helpers for full-text search index usage

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — add database migration creating GIN/GiST indexes on text columns used by the search service (SBOM names, advisory descriptions, package names)

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Inspect the current query patterns to identify missing indexes and suboptimal joins.
- Use the existing query builder helpers in `common/src/db/query.rs` for filtering, pagination, and sorting — extend them if needed rather than duplicating logic.
- Follow the SeaORM migration pattern established in `migration/src/m0001_initial/mod.rs` for the new migration file.
- The search endpoint is registered at `GET /api/v2/search` in `modules/search/src/endpoints/mod.rs` — verify that the endpoint benefits from the index changes.
- Per the repository's key conventions: use Axum for HTTP and SeaORM for database. All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Assumption pending clarification:** No specific latency targets were provided. The optimization targets adding proper indexes for text search columns and ensuring queries use them. The acceptance criteria include adding a verification query to confirm index usage.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — existing shared filtering, pagination, and sorting logic; extend for indexed full-text search rather than writing new query utilities
- `common/src/db/limiter.rs::connection pool limiter` — existing connection pool management; verify pool settings are adequate for search query load
- `migration/src/m0001_initial/mod.rs` — reference migration pattern for creating the new migration

## Acceptance Criteria
- [ ] Database migration creates appropriate indexes (GIN or GiST) on text columns used by the search service
- [ ] Search queries in SearchService use the new indexes (verified via EXPLAIN ANALYZE)
- [ ] Existing search functionality continues to work without regressions
- [ ] Migration runs successfully against a clean database and an existing database

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying that search queries return results after the migration is applied
- [ ] Verify that the migration applies cleanly (up) and can be rolled back (down)
- [ ] Add a test that performs a search query and confirms it completes (establishes baseline for future performance assertions)

## Verification Commands
- `cargo test -p tests --test search` — existing search tests pass
- `cargo run --bin migration -- up` — migration applies successfully

## Documentation Updates
- `README.md` — document the new migration and any changed search behavior

## Dependencies
- None
