## Repository

trustify-backend

## Target Branch

main

## Description

Optimize the search query performance in the `SearchService` to reduce response latency for the `GET /api/v2/search` endpoint. The current full-text search implementation is reported as "too slow" by users, though no specific latency baseline or target has been provided (see Assumptions below).

This task focuses on the database query layer: adding appropriate indexes for full-text search columns, optimizing the query construction in the search service, and applying pagination limits to prevent unbounded result sets.

**Assumptions (pending clarification):**
- **AMBIGUITY: No performance baseline or target defined.** The feature states search is "too slow" but provides no current latency measurements or target response times. This task assumes a target of sub-500ms p95 response time for typical search queries, pending stakeholder confirmation.
- **AMBIGUITY: Scope of "search" is undefined.** The feature does not specify whether "search" refers to the dedicated `/api/v2/search` endpoint, the list endpoints on individual modules (SBOM, advisory, package), or both. This task assumes the primary target is the `SearchService` full-text search endpoint at `/api/v2/search`, as that is the dedicated search module.

## Acceptance Criteria

- [ ] Search queries against `GET /api/v2/search` execute with reduced latency compared to current implementation
- [ ] Database migration adds appropriate indexes for full-text search columns
- [ ] Query builder uses indexed columns for search operations
- [ ] Pagination is enforced on search results to prevent unbounded queries
- [ ] Existing search functionality is not broken (all current search results remain accessible)
- [ ] Connection pool limiter settings are reviewed and tuned if necessary

## Files to Modify

- `modules/search/src/service/mod.rs` -- Optimize `SearchService` query construction for full-text search
- `common/src/db/query.rs` -- Review and optimize shared query builder helpers used by search
- `common/src/db/limiter.rs` -- Review connection pool limiter settings for search-heavy workloads

## Files to Create

- `migration/src/m0002_search_indexes/mod.rs` -- Database migration to add full-text search indexes

## Implementation Notes

- The `SearchService` in `modules/search/src/service/mod.rs` handles full-text search across entities. Optimize the query construction to use database-level full-text search indexes (e.g., PostgreSQL GIN/GiST indexes) rather than LIKE-based pattern matching if currently used.
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for creating the new migration module.
- Use the shared query builder helpers in `common/src/db/query.rs` for pagination and sorting to ensure search results are bounded. The existing `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` should be used for response formatting.
- Review `common/src/db/limiter.rs` to ensure the connection pool can handle concurrent search queries without starving other operations.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.
- Consider leveraging `tower-http` caching middleware for search results with appropriate cache TTL, following the caching pattern referenced in the Key Conventions.

**Convention: Error handling** -- Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope. All service methods must return `Result<T, AppError>` with `.context()` wrapping.

**Convention: Response types** -- Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's endpoint/service scope. Search results must use `PaginatedResults<T>` from `common/src/model/paginated.rs`.

**Convention: Query helpers** -- Applies: task modifies `common/src/db/query.rs` matching the convention's database query scope. Shared filtering, pagination, and sorting helpers must be used.

## Test Requirements

- Add integration tests in `tests/api/search.rs` verifying that search queries return results within acceptable time bounds
- Add tests verifying that paginated search results respect limit/offset parameters
- Add tests verifying that existing search functionality continues to return correct results after index changes
- Follow the existing integration test pattern using real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern
