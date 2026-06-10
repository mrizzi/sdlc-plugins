# Task 2 — Implement search relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Implement full-text search relevance ranking in the SearchService so that search results are ordered by relevance rather than insertion order or arbitrary ordering. The feature description says "results should be more relevant" and "users complain about irrelevant results" but provides no definition of relevance, no ranking criteria, and no examples of good vs bad results (**assumption pending clarification**: we will use PostgreSQL's `ts_rank` function with weighted text search vectors, prioritizing title/name fields over description/body fields). This task addresses the "Results should be more relevant" MVP requirement from TC-9002.

## Files to Modify
- `modules/search/src/service/mod.rs` — modify SearchService to implement `ts_rank`-based relevance scoring and ordering in search queries
- `modules/search/src/endpoints/mod.rs` — update the `GET /api/v2/search` endpoint to support an optional `sort=relevance` query parameter (default when a search query is provided)
- `common/src/db/query.rs` — extend query builder helpers to support relevance-based sorting alongside existing pagination and sorting

## API Changes
- `GET /api/v2/search` — MODIFY: add optional `sort` query parameter accepting `relevance` (default when `q` is provided) or `date`; response items now include a `relevance_score` field (float)

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Inspect how it currently constructs queries to understand where ranking can be injected.
- Use PostgreSQL's `ts_vector` and `ts_rank` (or `ts_rank_cd`) to compute relevance scores. Weight title/name fields (weight A) more heavily than description/body fields (weight D).
- The response type for list endpoints is `PaginatedResults<T>` from `common/src/model/paginated.rs` — the relevance score should be added to each search result item, not to the pagination wrapper.
- Per the repository's key conventions: list endpoints return `PaginatedResults<T>`; shared filtering, pagination, and sorting are in `common/src/db/query.rs`; all handlers return `Result<T, AppError>` with `.context()` wrapping.
- **Assumption pending clarification:** The ranking algorithm uses PostgreSQL ts_rank with field weighting (title > description). No specific relevance algorithm was specified in the feature. If the product owner provides a different ranking strategy, the implementation should be adjusted accordingly.
- **Assumption pending clarification:** We assume "more relevant" means ordering by text similarity score. The field weighting (names/titles weighted higher) is an assumption that should be validated with the product owner.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — existing shared sorting logic; extend to support `ts_rank`-based ordering
- `common/src/model/paginated.rs::PaginatedResults<T>` — existing response wrapper; search results will continue using this wrapper
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService::search` — existing search method on advisories; inspect for patterns to reuse or align with

## Acceptance Criteria
- [ ] Search results are ordered by relevance score when a text query is provided
- [ ] The relevance ranking prioritizes matches in title/name fields over description/body fields
- [ ] An optional `sort` query parameter allows switching between relevance and date ordering
- [ ] Each search result item includes a `relevance_score` field
- [ ] Existing search functionality (without explicit sort parameter) continues to work, defaulting to relevance ordering

## Test Requirements
- [ ] Integration test verifying that a search for a term appearing in a title ranks that result higher than a result where the term only appears in the description
- [ ] Integration test verifying the `sort=relevance` and `sort=date` query parameters work correctly
- [ ] Integration test verifying backward compatibility — search without a `sort` parameter returns results (defaulting to relevance)

## Verification Commands
- `cargo test -p tests --test search` — all search tests pass including new relevance tests

## Dependencies
- Depends on: Task 1 — Optimize search query performance (indexes should be in place before adding ranking)
