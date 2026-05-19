## Repository
trustify-backend

## Target Branch
main

## Description
Replace the current search implementation with PostgreSQL full-text search queries that leverage the tsvector indexes created in Task 1. Search results will be ranked by relevance using `ts_rank`, so that the most relevant matches appear first. This directly addresses the "results should be more relevant" and "search should be faster" requirements from TC-9002.

**Assumption (pending clarification -- see A2, A7 in impact map):** "More relevant" is interpreted as PostgreSQL full-text ranking via `ts_rank`. The current search implementation is assumed to use basic pattern matching (LIKE/ILIKE). If the current implementation already uses a different ranking strategy, this task should be re-evaluated. The specific ranking weights and boosting factors are not specified in the feature description and are set to sensible defaults; these may need tuning based on user feedback.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Rewrite `SearchService` query logic to use `to_tsquery` and `ts_rank` instead of LIKE/ILIKE; order results by relevance score; include score in results
- `modules/search/src/endpoints/mod.rs` -- Add optional `sort` query parameter to allow sorting by relevance (default) or other fields; ensure backward compatibility (existing query parameter `q` continues to work)
- `tests/api/search.rs` -- Update existing search tests and add new tests for relevance ranking

## API Changes
- `GET /api/v2/search` -- MODIFY: Results are now ranked by relevance by default. Add optional `sort` query parameter (values: `relevance`, `name`, `date`; default: `relevance`). Response shape unchanged (still `PaginatedResults<T>`). Backward compatible -- existing clients see improved ordering without changes.

## Implementation Notes
- In `modules/search/src/service/mod.rs`, replace the existing search query with a full-text search query:
  - Use `to_tsquery('english', ...)` to parse the user's search input (use the helper from `common/src/db/query.rs` added in Task 1)
  - Use `ts_rank(search_vector, query)` to score results (use the helper from Task 1)
  - Search across all three entity types (sbom, advisory, package) as the current `SearchService` does
  - Order by `ts_rank` descending by default
- Follow the existing endpoint patterns in `modules/search/src/endpoints/mod.rs` -- look at how list endpoints in `modules/fundamental/src/advisory/endpoints/list.rs` handle query parameters for pagination and sorting
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response (already in use)
- Handle edge cases: empty search string (return all results, no ranking), special characters in search input (the tsquery builder from Task 1 should sanitize these)
- Preserve the existing `q` query parameter for the search string -- do not rename or remove it
- The `sort` parameter should be an enum deserialized from the query string, following the pattern used in other endpoints

## Reuse Candidates
- `common/src/db/query.rs` -- Full-text search helpers (tsquery construction, ts_rank scoring) added in Task 1
- `common/src/model/paginated.rs::PaginatedResults<T>` -- Already used by search; continue using for ranked results
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Pattern for query parameter parsing (pagination, sorting) to follow for the new `sort` parameter
- `common/src/error.rs::AppError` -- Error handling for invalid search input

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsvector`/`tsquery`) instead of pattern matching
- [ ] Results are ranked by relevance score (`ts_rank`) by default
- [ ] The `sort` query parameter allows sorting by `relevance`, `name`, or `date`
- [ ] Existing `q` query parameter continues to work unchanged
- [ ] Empty search string returns all results (no error)
- [ ] Special characters in search input are handled gracefully (no SQL errors)
- [ ] Response format remains `PaginatedResults<T>` -- backward compatible
- [ ] Search performance is improved compared to LIKE-based queries (verified by query plan using EXPLAIN)
- [ ] All existing search tests continue to pass

## Test Requirements
- [ ] Integration test: search with a term that matches multiple entities, verify results are ordered by relevance
- [ ] Integration test: search with `sort=name`, verify alphabetical ordering
- [ ] Integration test: search with empty string, verify all results returned
- [ ] Integration test: search with special characters (`&`, `|`, `!`, `:`, `'`), verify no errors
- [ ] Integration test: verify `PaginatedResults` pagination works with ranked results

## Verification Commands
- `cargo test --test api` -- all integration tests pass including new search relevance tests

## Dependencies
- Depends on: Task 1 -- Add full-text search indexes and tsvector migration
