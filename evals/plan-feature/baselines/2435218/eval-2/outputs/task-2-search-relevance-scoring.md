# Task 2 — Add field-weighted relevance scoring to search results

**Feature:** TC-9002 — Improve search experience
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Description
Improve search result relevance by adding field-weighted scoring to the `SearchService`. Currently, the full-text search across entities treats all fields equally. This task adds weighted scoring so that matches in high-signal fields (e.g., name, title, identifier) rank higher than matches in lower-signal fields (e.g., description, content body).

**Ambiguity flag:** The feature does not define what "relevant" means. This task assumes relevance means: (1) title/name matches rank higher than description matches, (2) exact matches rank higher than partial matches, and (3) results are ordered by relevance score descending. The product owner should confirm whether additional ranking factors (e.g., recency, severity) are desired.

## Files to Modify
- `modules/search/src/service/mod.rs` — Modify `SearchService` to add weighted scoring to search queries using `ts_rank_cd` or equivalent PostgreSQL ranking functions with field weights
- `modules/search/src/endpoints/mod.rs` — Ensure the search endpoint returns results ordered by relevance score by default

## Implementation Notes
- Inspect the current `SearchService` implementation in `modules/search/src/service/mod.rs` to understand the existing query structure before modifying
- Use PostgreSQL `ts_rank_cd()` with weight vectors (e.g., weight A for name/title, weight B for description) to compute relevance scores
- The search endpoint at `GET /api/v2/search` (defined in `modules/search/src/endpoints/mod.rs`) should default to ordering by relevance score when no explicit sort is provided
- Reference the existing sorting pattern in `common/src/db/query.rs` to understand how sorting is currently implemented in list endpoints
- Ensure the relevance score does not break the existing `PaginatedResults<T>` response wrapper in `common/src/model/paginated.rs`
- Per docs/constraints.md Section 5.4: do not duplicate existing sorting/query logic — reuse or extend `common/src/db/query.rs` utilities
- Per docs/constraints.md Section 2 (Commit Rules): commit must reference TC-9002 in the footer

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder with existing sorting support; extend rather than duplicate
- `common/src/model/paginated.rs` — `PaginatedResults<T>` wrapper for paginated responses
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` search method may show an existing pattern for search-with-ranking

## Acceptance Criteria
- [ ] Search results are returned ordered by relevance score (highest first) by default
- [ ] Title/name field matches produce higher relevance scores than description-only matches
- [ ] Exact phrase matches produce higher scores than partial word matches
- [ ] Existing search functionality is not broken (all current tests pass)
- [ ] The relevance ordering can be overridden by explicit sort parameters

## Test Requirements
- [ ] Integration test: search for a term that appears in one entity's name and another entity's description — verify the name-match entity ranks higher
- [ ] Integration test: search for an exact phrase vs partial match — verify exact phrase ranks higher
- [ ] Integration test: verify default sort is by relevance when no sort parameter is provided
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test -p tests --test search` — search tests pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (indexes must exist for efficient ranked queries)
