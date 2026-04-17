# Task 2 — Improve search result ranking with full-text scoring

## Repository
trustify-backend

## Description
Improve the relevance of search results by incorporating PostgreSQL full-text
ranking (`ts_rank` or `ts_rank_cd`) into the search query. The current
`SearchService` in `modules/search/src/service/mod.rs` performs full-text search
but the feature states "results should be more relevant" without defining what
"relevant" means.

**Ambiguity note:** "More relevant" is not defined in the feature. This task
assumes relevance means better full-text match scoring using PostgreSQL's built-in
ranking functions. It does NOT implement: fuzzy matching, typo tolerance, synonym
support, ML-based ranking, or recency/severity weighting. If the stakeholder's
definition of "relevant" includes any of those, additional tasks will be needed.
The implementer should document the ranking approach chosen so the stakeholder can
evaluate whether it matches their expectations.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add `ts_rank` scoring to search queries and order results by rank
- `modules/search/src/endpoints/mod.rs` — Pass ranking-related parameters through to the service layer if needed

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` handles full-text search; extend it rather than replacing it
- Use PostgreSQL `ts_rank(tsvector_column, to_tsquery(search_term))` to score results and `ORDER BY` the rank descending
- The `common/src/db/query.rs` module provides shared query builder helpers for filtering, pagination, and sorting; the ranking query should integrate with this existing infrastructure rather than bypassing it
- Results should still be returned as `PaginatedResults<T>` using the wrapper from `common/src/model/paginated.rs`
- Error handling must follow the `Result<T, AppError>` pattern with `.context()` wrapping per the project conventions
- **Ambiguity:** Without knowing how the current search query is structured (single-entity vs. cross-entity union), the exact integration point for `ts_rank` is unclear. The implementer must inspect the current query in `SearchService` before modifying it
- Per constraints doc section 5: changes must be scoped to the files listed; do not refactor unrelated code

## Reuse Candidates
- `common/src/db/query.rs` — Query builder helpers for filtering, pagination, sorting; ranking should integrate with existing sorting infrastructure
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper; search results must continue to use this type

## Acceptance Criteria
- [ ] Search results are ordered by full-text relevance score (best matches first)
- [ ] The ranking does not break the existing search response shape (`PaginatedResults<T>`)
- [ ] Existing search queries that previously returned results continue to return the same results (order may change)
- [ ] The search endpoint remains backward compatible (existing query parameters still work)

## Test Requirements
- [ ] Integration test verifying that a more precise search term ranks higher than a partial match
- [ ] Integration test verifying that existing search functionality still returns results (backward compatibility)
- [ ] Existing `tests/api/search.rs` tests continue to pass

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (indexes should be in place for ranking queries to perform well)
