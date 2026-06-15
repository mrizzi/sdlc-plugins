## Repository
trustify-backend

## Target Branch
main

## Description
Replace the current search implementation in `SearchService` with PostgreSQL full-text search using `tsvector`/`tsquery` to improve result relevance. The current search (in `modules/search/src/service/mod.rs`) returns results that users report as irrelevant. This task implements ranked full-text search using `ts_rank` scoring against the `tsvector` columns created in Task 1, so that results are ordered by relevance rather than insertion order or alphabetical sorting.

**Assumptions pending clarification:**
- Relevance ranking uses PostgreSQL's built-in `ts_rank` with default weights as a baseline. The feature description provides no ranking algorithm, weighting factors, or examples of "relevant" vs. "irrelevant" results. This strategy needs product review.
- Search covers all three entity types (SBOMs, advisories, packages) in a single query. The feature does not specify whether search should be entity-specific or cross-entity. Assumption is cross-entity, matching the current behavior of `GET /api/v2/search`.
- The search language configuration is assumed to be `'english'` for the text search dictionary. No language requirements were specified.

## Files to Modify
- `modules/search/src/service/mod.rs` — Replace existing search logic with `tsvector`/`tsquery` full-text search using `ts_rank` for relevance scoring
- `modules/search/src/endpoints/mod.rs` — Update the search endpoint handler to pass through relevance-sorted results from the updated service

## Implementation Notes
- The `SearchService` in `modules/search/src/service/mod.rs` currently performs full-text search across entities. Replace the query mechanism with PostgreSQL `to_tsquery()` and `ts_rank()` against the `tsvector` columns added by Task 1.
- Use `plainto_tsquery('english', <user_input>)` for user-friendly query parsing (handles plain text without requiring special syntax).
- Order results by `ts_rank(tsvector_column, query)` descending so the most relevant results appear first.
- The endpoint in `modules/search/src/endpoints/mod.rs` currently returns search results via the `GET /api/v2/search` route. Ensure the response continues to use `PaginatedResults<T>` from `common/src/model/paginated.rs` for backward compatibility.
- Use the query builder helpers in `common/src/db/query.rs` for pagination and sorting integration with the new relevance-based ordering.
- All handlers must continue to return `Result<T, AppError>` with `.context()` wrapping per the project's error handling pattern (see `common/src/error.rs`).

## Reuse Candidates
- `common/src/db/query.rs` — Existing query builder helpers for filtering, pagination, and sorting that should be extended/reused for the new relevance-scored queries
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper that must be preserved for backward compatibility
- `common/src/error.rs::AppError` — Error handling pattern used across all service methods

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsvector`/`tsquery`) instead of the previous search mechanism
- [ ] Results are ranked by relevance using `ts_rank` scoring, with most relevant results first
- [ ] The `GET /api/v2/search` endpoint continues to return `PaginatedResults<T>` with the same response shape (backward compatible)
- [ ] Search handles multi-word queries correctly (e.g., "security vulnerability" matches documents containing both terms)
- [ ] Empty or whitespace-only search queries return a meaningful response (empty results or validation error) rather than a server error

## Test Requirements
- [ ] Integration test: search for a known term returns the expected entity as the top result
- [ ] Integration test: search results are ordered by relevance (a document with the search term in the title ranks higher than one with the term only in the description)
- [ ] Integration test: multi-word query returns results matching all terms
- [ ] Integration test: empty search query returns an appropriate response (empty results or 400 error)
- [ ] Existing tests in `tests/api/search.rs` continue to pass or are updated to reflect the new ranking behavior

## Dependencies
- Depends on: Task 1 — Add search indexes (requires `tsvector` columns and GIN indexes to exist)

[sdlc-workflow] Description digest: sha256-md:2fa1e4901ac3298496076cc56085d940afa4549495a86878cc3cd2669bd801f3
