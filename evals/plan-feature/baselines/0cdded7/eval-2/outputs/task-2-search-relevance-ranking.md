## Repository
trustify-backend

## Target Branch
main

## Description
Extend the SearchService to support weighted full-text search ranking, so that search results are ordered by relevance rather than by insertion order. This addresses TC-9002 requirement: "Results should be more relevant." Title/name matches are weighted higher than description matches, and results include a relevance score. The search service will use PostgreSQL's `ts_rank` function with the GIN indexes added in Task 1.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor SearchService to use `ts_rank()` weighted full-text search instead of simple LIKE/ILIKE queries; add per-entity relevance scoring with title matches weighted higher (weight A) than description matches (weight D)
- `modules/search/src/endpoints/mod.rs` — update the GET /api/v2/search handler to pass ranking parameters to SearchService and return results sorted by relevance score

## API Changes
- `GET /api/v2/search` — MODIFY: response now includes a `relevance_score` field per result and results are sorted by relevance descending by default

## Implementation Notes
- Use PostgreSQL's `ts_rank(tsvector, tsquery, weights)` function to compute relevance. Assign weight A (1.0) to name/title columns and weight D (0.1) to description columns.
- Build the `tsquery` from the user's search input using `plainto_tsquery('english', $1)` for robust tokenization.
- The existing `SearchService` in `modules/search/src/service/mod.rs` currently does full-text search across entities — extend it rather than replacing it. Preserve the multi-entity search behavior.
- Use `common/src/db/query.rs` query builder helpers for constructing the ranked query. Check whether existing pagination helpers in `common/src/model/paginated.rs` (`PaginatedResults<T>`) can carry the relevance score, or if the result struct needs a wrapper.
- Reference the error handling pattern from `common/src/error.rs` (`AppError` with `.context()` wrapping) for any new error paths.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; extend rather than duplicate for ranked queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; may need to be extended or wrapped to include relevance score
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` search method as a reference for existing search patterns in the codebase

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (descending) by default
- [ ] Title/name matches rank higher than description-only matches
- [ ] Each result in the response includes a `relevance_score` numeric field
- [ ] Existing search functionality (basic keyword search) continues to work
- [ ] Response format remains compatible with `PaginatedResults` pattern

## Test Requirements
- [ ] Integration test: a search for a term appearing in a title ranks that result above a result where the term only appears in the description
- [ ] Integration test: search with no results returns an empty paginated response (not an error)
- [ ] Integration test: relevance_score is present and is a positive number for matching results
- [ ] Existing search tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add search indexes (GIN indexes must exist for ts_rank to be efficient)

[sdlc-workflow] Description digest: sha256:57ac5fb7e124974c84bec12f16ab4dc6a387f6502b977f7a803ac057e6bcd0b6
