## Repository
trustify-backend

## Description
Optimize the `SearchService` to use PostgreSQL full-text search with relevance ranking instead of basic text matching. This task replaces the current search implementation with `to_tsquery`-based queries against the `tsvector` columns created in Task 1, and ranks results using `ts_rank` so that the most relevant results appear first. This directly addresses the user complaints about irrelevant search results and slow search performance described in TC-9002.

**Ambiguity note:** "Relevance" is not defined in the feature description. This task assumes relevance means PostgreSQL `ts_rank` scoring based on full-text match quality. The ranking algorithm may need refinement after user testing — this assumption is pending clarification.

## Files to Modify
- `modules/search/src/service/mod.rs` — Rewrite `SearchService` search method to use `to_tsquery` against `search_vector` columns with `ts_rank` ordering instead of basic text matching
- `common/src/db/query.rs` — Add full-text search query helper functions (tsquery construction, ts_rank ordering) to the shared query builder

## Files to Create
- `common/src/db/full_text.rs` — Full-text search utility module providing helper functions for tsquery construction, search vector matching, and relevance ranking

## API Changes
- `GET /api/v2/search` — MODIFY: Response results are now ordered by relevance score (descending) when a search query is provided. An optional `relevance_score` field is added to each result item. Backward compatible — existing callers receive the same response shape with improved ordering.

## Implementation Notes
- The current search implementation is in `modules/search/src/service/mod.rs` (`SearchService: full-text search across entities`). Replace the existing query logic with PostgreSQL full-text search operators.
- Use `plainto_tsquery('english', ?)` to parse user search input safely (handles plain text without requiring tsquery syntax from the user).
- Use `ts_rank(search_vector, query)` to compute relevance scores and order results by descending rank.
- Create a new utility module `common/src/db/full_text.rs` with helper functions:
  - `build_tsquery(input: &str) -> String` — sanitizes and converts user input to a tsquery expression
  - `rank_expression(vector_column: &str, query: &str) -> String` — generates the `ts_rank()` SQL expression
- Register `full_text.rs` in `common/src/db/mod.rs`.
- Follow the existing error handling pattern: all handlers return `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs` for `AppError` definition).
- The search endpoint returns `PaginatedResults<T>` (from `common/src/model/paginated.rs`) — maintain this response wrapper.
- Follow the existing module pattern: `model/ + service/ + endpoints/` structure as used throughout `modules/fundamental/`.
- The search endpoint is registered at `GET /api/v2/search` in `modules/search/src/endpoints/mod.rs` — the route path and HTTP method must remain unchanged for backward compatibility.
- Consider the `tower-http` caching middleware noted in the repository conventions — search results with query parameters should have appropriate cache headers (likely `no-cache` or short TTL for dynamic search results).

## Reuse Candidates
- `common/src/db/query.rs` — Existing shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate for full-text search support
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper to use for search results
- `common/src/error.rs` — `AppError` enum for error handling pattern
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` has an existing `search` method that may contain patterns to reference or align with

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`to_tsquery` / `plainto_tsquery`) against `search_vector` columns
- [ ] Search results are ranked by relevance using `ts_rank` and returned in descending relevance order
- [ ] Search queries that previously returned results continue to return results (backward compatibility)
- [ ] The search endpoint response time improves compared to baseline for typical queries
- [ ] The `GET /api/v2/search` endpoint path and basic response shape remain unchanged
- [ ] Full-text search helper functions are available in `common/src/db/full_text.rs` for reuse by other modules
- [ ] Error handling follows the `Result<T, AppError>` with `.context()` pattern

## Test Requirements
- [ ] Integration test verifying that a search query returns results ordered by relevance (most relevant first)
- [ ] Integration test verifying that a search with no matches returns an empty `PaginatedResults` (not an error)
- [ ] Integration test verifying backward compatibility: search with an existing query term returns results in the same response format
- [ ] Integration test verifying that search spans SBOMs, advisories, and packages (cross-entity search)
- [ ] Unit test for `build_tsquery` helper function: verifies safe handling of special characters, empty input, and multi-word queries

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test -p common` — common module tests pass (new full_text helpers)

## Dependencies
- Depends on: Task 1 — Add database migration for full-text search indexes
