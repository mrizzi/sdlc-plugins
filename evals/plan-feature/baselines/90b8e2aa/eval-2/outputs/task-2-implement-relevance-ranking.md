## Repository
trustify-backend

## Target Branch
main

## Description
Implement search result relevance ranking in the SearchService so that results are ordered by textual match quality rather than an arbitrary default order. The current full-text search in `modules/search/src/service/mod.rs` returns results without a relevance score, which means users see results in an order that does not reflect how well each result matches their query.

This task addresses the "results should be more relevant" requirement from TC-9002. **Assumption (pending clarification):** "more relevant" means applying PostgreSQL ts_rank scoring to order results by text match quality. No specific ranking algorithm, field weighting scheme, or relevance scoring formula was provided in the feature description.

## Files to Modify
- `modules/search/src/service/mod.rs` — modify SearchService to use `ts_rank` or `ts_rank_cd` for scoring search results and ordering by relevance score descending
- `modules/search/src/endpoints/mod.rs` — expose relevance score in the search response so consumers can display or use it

## Implementation Notes
- Use PostgreSQL `ts_rank(to_tsvector('english', column), plainto_tsquery('english', query))` to compute relevance scores per result row.
- Combine scores across multiple columns (e.g., SBOM name, advisory title, package name) using weighted addition — assign higher weight to title/name fields than description fields.
- Add the relevance score as an optional field in the search response. Follow the existing response pattern using `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Error handling: all search operations must return `Result<T, AppError>` with `.context()` wrapping per project conventions. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust source file scope.
- The existing `common/src/db/query.rs` provides shared sorting helpers — extend or reuse the sorting mechanism to support `ORDER BY relevance_score DESC` as the default sort when a search query is present.
- Maintain backward compatibility: when no search query text is provided (e.g., listing all items), fall back to the previous default ordering so existing clients are not affected.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers with existing sorting support; extend for relevance-based sorting
- `common/src/model/paginated.rs` — PaginatedResults<T> wrapper used by all list endpoints; search results should follow this pattern
- `common/src/error.rs` — AppError enum for consistent error handling

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest match quality first) when a query string is provided
- [ ] Relevance score is included in the search response for each result
- [ ] When no query string is provided, results maintain their previous default ordering (backward compatible)
- [ ] Results that match in title/name fields rank higher than results matching only in description fields

## Test Requirements
- [ ] Integration test: search for a known term and verify results are ordered by relevance (a result with the term in the title ranks above one with the term only in the description)
- [ ] Integration test: search without a query string returns results in default order (backward compatibility)
- [ ] Integration test: verify relevance score field is present in the response body

## Verification Commands
- `cargo test -p tests --test search` — search integration tests pass
- `cargo test -p fundamental` — module-level tests pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search query performance (GIN indexes enable efficient ts_rank computation)
