## Repository
trustify-backend

## Description
Improve the `SearchService` in `modules/search/src/service/mod.rs` to use full-text search with relevance scoring instead of naive text matching, and to support filter parameters for narrowing results. The current search service performs full-text search across entities but users report it is slow and returns irrelevant results. This task rewrites the core search logic to leverage the tsvector indexes (Task 1) and the new query builder helpers (Task 2).

**Assumption (pending clarification):** The search service is assumed to search across all three entity types (SBOMs, advisories, packages) and return a unified result set. The feature description does not specify whether cross-entity search, entity-specific search, or both is desired.

**Assumption (pending clarification):** Result ordering is assumed to be by relevance score (ts_rank) descending by default, with an option to sort by date or name. No specific ranking formula or boosting rules were specified.

## Files to Modify
- `modules/search/src/service/mod.rs` — Rewrite search query logic to use tsquery against tsvector columns with ts_rank scoring; accept and apply filter parameters; return results ordered by relevance
- `modules/search/src/lib.rs` — Update module exports if new types are introduced

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities — refactor its query construction to use the new `common/src/db/search.rs` helpers from Task 2
- Use `ts_rank(table.search_vector, plainto_tsquery('english', user_query))` for scoring, applied to each entity table (sbom, advisory, package)
- Compose the search query using helpers from `common/src/db/query.rs` for pagination and sorting, and `common/src/db/search.rs` for full-text search construction
- Apply filters before the full-text search to reduce the result set early (filter pushdown)
- Maintain the existing return type contract — results should still be compatible with `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Follow the error handling pattern from `common/src/error.rs` — wrap database errors with `.context()` for clear error messages
- Consider adding query plan hints or `SET` statements to encourage index usage if the query planner does not automatically choose the GIN index

## Reuse Candidates
- `common/src/db/search.rs` — Full-text search helpers (tsquery construction, ts_rank ordering) from Task 2
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper for paginated results
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Pattern for service methods that accept filter/query parameters
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — Pattern for service methods with list/fetch operations

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (tsquery/tsvector) instead of LIKE/ILIKE patterns
- [ ] Results are ordered by relevance score by default
- [ ] Filter parameters are accepted and applied to narrow search results
- [ ] Search returns results from SBOMs, advisories, and packages in a unified result set
- [ ] Search performance is improved for typical queries (GIN index is utilized)
- [ ] Existing SearchService public API contract is preserved or extended backward-compatibly

## Test Requirements
- [ ] Unit test: search with a specific term returns matching entities ranked by relevance
- [ ] Unit test: search with filters returns only entities matching both the search term and filters
- [ ] Unit test: empty search term with filters returns filtered results without full-text matching
- [ ] Unit test: search with no results returns empty paginated response

## Verification Commands
- `cargo test -p search` — Search module tests pass
- `cargo check -p search` — Search module compiles without warnings

## Dependencies
- Depends on: Task 2 — Extend query builder with filter and relevance support
