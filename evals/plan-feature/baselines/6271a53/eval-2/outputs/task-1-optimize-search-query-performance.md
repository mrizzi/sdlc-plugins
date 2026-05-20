# Task 1 — Optimize search query performance

**Feature:** TC-9002 — Improve search experience
**Label:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Search is currently reported as too slow. This task addresses the performance side of the search experience by adding database indexes to support full-text search queries and optimizing the query execution path in `SearchService`. The goal is to reduce search query latency by ensuring the database can efficiently execute text-matching queries across SBOMs, advisories, and packages.

## Files to Modify
- `modules/search/src/service/mod.rs` — Optimize query construction in `SearchService` to use indexed columns and avoid full table scans; apply query builder helpers from `common/src/db/query.rs` for pagination and sorting
- `common/src/db/query.rs` — Extend shared query builder to support full-text search predicates (e.g., `tsvector`/`tsquery` for PostgreSQL) that the search service can invoke
- `migration/src/lib.rs` — Register the new migration module

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Add a database migration that creates GIN indexes on text columns used by the search service (e.g., SBOM name/description, advisory title/description, package name) and adds `tsvector` generated columns where appropriate

## API Changes
- `GET /api/v2/search` — MODIFY: No contract change; response shape remains the same but query execution is faster due to index-backed full-text search

## Implementation Notes
- **Framework conventions:** Axum for HTTP, SeaORM for database. All handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Query helpers:** Use the shared filtering, pagination, and sorting utilities in `common/src/db/query.rs` rather than writing custom query logic. Extend `query.rs` with a full-text search predicate builder that wraps PostgreSQL `to_tsvector`/`to_tsquery` functions.
- **Migration pattern:** Follow the existing migration structure in `migration/src/m0001_initial/mod.rs`. The new migration should create GIN indexes on relevant text columns across the `sbom`, `advisory`, and `package` entities defined in `entity/src/`.
- **Entity references:** Review column definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify which text columns should be indexed for search.
- **Caching:** The search endpoint uses `tower-http` caching middleware. Verify that cache headers remain appropriate after performance changes — faster queries may warrant shorter cache TTLs.
- **Constraint §5.2:** Do not modify code without first inspecting it. Read the current `SearchService` implementation before changing query logic.
- **Constraint §5.4:** Reuse existing utilities — extend `common/src/db/query.rs` rather than duplicating query builder logic in the search module.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Shared filtering, pagination, and sorting utilities that should be extended (not duplicated) for full-text search
- `common/src/db/limiter.rs::connection pool limiter` — Connection pool management that may need tuning if search queries are resource-intensive
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper already used by list endpoints; search results should use the same type

## Acceptance Criteria
- [ ] A database migration exists that creates GIN indexes on text columns used by search
- [ ] `SearchService` queries leverage the new indexes for full-text search
- [ ] `common/src/db/query.rs` includes a reusable full-text search predicate builder
- [ ] Search queries execute significantly faster than before (observable in test database)
- [ ] Existing search functionality is not broken — all current search behavior is preserved

## Test Requirements
- [ ] Add integration test in `tests/api/search.rs` verifying that search returns correct results after index migration
- [ ] Add integration test confirming that the migration applies cleanly on a fresh database
- [ ] Verify that existing search tests continue to pass

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass
- `cargo run --bin migration` — migration applies without errors

## Documentation Updates
- `README.md` — Document the new migration step if setup instructions reference migrations
