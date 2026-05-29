## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the SearchService to use PostgreSQL full-text search (tsvector/tsquery) instead of the current search implementation, improving both performance and relevance of search results. This addresses the TC-9002 requirements for faster and more relevant search.

**Ambiguity note:** The feature description states "results should be more relevant" without defining relevance criteria or ranking preferences. **Assumption pending clarification:** We implement relevance ranking using PostgreSQL `ts_rank_cd()` with the following field weighting:
- Title/name fields: weight A (highest)
- Description fields: weight B
- Other metadata fields: weight C

This weighting scheme assumes users primarily search by name/title. The ranking algorithm and weights should be validated with the product owner.

**Ambiguity note:** The feature description does not specify which entity types should be included in search results. **Assumption pending clarification:** We include SBOMs, advisories, and packages — the three primary entities in the current search endpoint — in the unified search results.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace current search implementation with tsvector/tsquery-based full-text search, add relevance ranking with `ts_rank_cd()`
- `modules/search/src/endpoints/mod.rs` — update endpoint handler to pass search query to the refactored SearchService and return ranked results

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` implements `full-text search across entities` per the repository structure — inspect the current implementation to understand the existing query pattern before refactoring
- Use PostgreSQL `to_tsquery('english', ...)` or `plainto_tsquery('english', ...)` to parse user search input. Prefer `plainto_tsquery` for simple keyword search and `websearch_to_tsquery` if available for more natural query syntax
- Rank results using `ts_rank_cd(search_vector, query)` and order by rank descending
- The query should search across the tsvector columns created in Task 1 on sbom, advisory, and package tables
- Use UNION ALL to combine results from different entity tables, each with their own relevance score, then sort the combined results by score
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for service method structure — methods return `Result<T, AppError>` using error handling from `common/src/error.rs`
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response wrapper, consistent with all other list endpoints
- Leverage query builder helpers from `common/src/db/query.rs` for pagination and sorting
- Per docs/constraints.md §2 (Commit Rules): use Conventional Commits format with Jira issue ID in footer
- Per docs/constraints.md §5.4: reuse existing utilities in `common/src/db/query.rs` rather than duplicating query building logic

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend for full-text search rather than building from scratch
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper used by all list endpoints
- `common/src/error.rs` — `AppError` enum for consistent error handling
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation of a service module showing fetch/list patterns
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` which already has a `search` method that may contain patterns to follow or extend

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (tsvector/tsquery) instead of the previous implementation
- [ ] Search results are ranked by relevance using `ts_rank_cd()` with field weighting
- [ ] Search returns results from SBOMs, advisories, and packages in a unified ranked list
- [ ] Search response time is measurably improved over the current implementation (target: sub-500ms p95 — assumption pending clarification on performance targets)
- [ ] Empty search queries return a meaningful default (e.g., most recent items or an error)
- [ ] Existing `GET /api/v2/search` endpoint contract is preserved (no breaking changes to response shape)

## Test Requirements
- [ ] Integration test: search for a known SBOM name returns that SBOM in results
- [ ] Integration test: search for a known advisory title returns that advisory in results
- [ ] Integration test: search for a known package name returns that package in results
- [ ] Integration test: results are ordered by relevance (exact title match ranks higher than partial description match)
- [ ] Integration test: empty or whitespace-only search query is handled gracefully
- [ ] Existing tests in `tests/api/search.rs` pass or are updated to reflect the improved behavior

## Verification Commands
- `cargo test --test api search` — search integration tests pass
- `cargo test --test api` — all integration tests pass (no regression)

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (requires tsvector columns and GIN indexes to exist)

[sdlc-workflow] Description digest: sha256:4b5af7557e703c458073eca82cd92983deaf4c414ccb69c97628c131e33ec395
