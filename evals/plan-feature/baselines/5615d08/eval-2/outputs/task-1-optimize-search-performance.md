## Repository
trustify-backend

## Description
Optimize the search query performance in the `SearchService` to reduce response latency for the `GET /api/v2/search` endpoint. The feature requirement states search is "currently too slow" but provides no specific latency target (see Ambiguity A1 in impact-map.md). This task addresses the structural performance improvements: adding database indexes for full-text search columns and optimizing the query execution path in the search service.

**Assumption (pending clarification):** No specific latency SLA has been defined. This task targets measurable improvement over the current baseline, which should be established before implementation begins by benchmarking the existing endpoint.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize the `SearchService` query execution: reduce redundant queries, add query plan hints, and batch entity lookups where possible
- `common/src/db/query.rs` — Add search-optimized query builder methods that leverage database indexes and avoid full table scans

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration to add GIN/GiST indexes on full-text search columns across sbom, advisory, and package tables

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Review the current query patterns to identify N+1 queries or missing index usage.
- The shared query builder in `common/src/db/query.rs` provides filtering, pagination, and sorting helpers. Add a new method (e.g., `apply_search_optimization`) that configures query hints for the PostgreSQL planner when full-text search predicates are present.
- Follow the SeaORM migration pattern established in `migration/src/m0001_initial/mod.rs` for the new migration module. Register the new migration in `migration/src/lib.rs`.
- The entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` define the columns that need indexing. Add GIN indexes on text columns used for search (e.g., name, description fields).
- Use PostgreSQL `to_tsvector` / `to_tsquery` patterns if not already in use, or add indexes that support the existing search predicates.
- The connection pool limiter in `common/src/db/limiter.rs` should be reviewed to ensure search queries are not being unnecessarily throttled.

## Reuse Candidates
- `common/src/db/query.rs::apply_filtering` — Existing filtering helper; extend rather than duplicate for search-specific optimizations
- `common/src/model/paginated.rs::PaginatedResults` — Existing response wrapper; no changes needed for this task

## Acceptance Criteria
- [ ] Database migration adds appropriate indexes for full-text search on sbom, advisory, and package tables
- [ ] Search queries in `SearchService` use indexed columns and avoid full table scans
- [ ] The `GET /api/v2/search` endpoint returns the same results as before (no regression in result content)
- [ ] Query execution time is measurably reduced (verified by comparing EXPLAIN ANALYZE output before and after)
- [ ] Migration runs successfully against a clean database and an existing database with data

## Test Requirements
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass (regression check)
- [ ] New migration applies cleanly in the test database setup
- [ ] EXPLAIN ANALYZE confirms index usage for typical search queries (manual verification step)

## Verification Commands
- `cargo test --test search` — existing search tests pass
- `cargo run --bin migration` — migration applies without errors

## Dependencies
- Depends on: None
