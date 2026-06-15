## Repository
trustify-backend

## Target Branch
main

## Description
Improve the SearchService to return results ranked by relevance instead of an unspecified default order. This addresses the "results should be more relevant" requirement by implementing text-match-quality-based ranking using PostgreSQL's full-text search ranking functions.

Assumption (pending clarification): The feature does not define what "relevant" means. This task assumes relevance is determined by text match quality (ts_rank) as the primary signal. It does not implement recency-based or severity-based ranking without explicit requirements, though the design should allow adding additional ranking signals later.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor SearchService to use PostgreSQL `ts_rank` or `ts_rank_cd` for result ordering, replace any naive LIKE/ILIKE queries with `to_tsvector`/`to_tsquery` based full-text search
- `common/src/db/query.rs` — Add shared helper for building ranked full-text search queries that can be reused by other services

## Implementation Notes
In `modules/search/src/service/mod.rs` (SearchService):
- Replace existing search implementation with PostgreSQL full-text search using `to_tsvector` and `to_tsquery`
- Use `ts_rank` or `ts_rank_cd` to compute a relevance score for each result
- Order results by relevance score descending by default
- Ensure exact matches on identifiers (CVE IDs, SBOM names) rank highest — use `plainto_tsquery` for user input and boost exact matches

Assumption (pending clarification): Without knowing which search scenarios are broken today, this implementation applies ranking uniformly across all entity types (SBOMs, advisories, packages). If certain entity types need different ranking strategies, that should be specified.

In `common/src/db/query.rs`:
- Add a `FullTextSearchBuilder` or equivalent helper struct that encapsulates tsvector/tsquery construction and ranking
- This helper should integrate with the existing query builder pattern used for filtering, pagination, and sorting

Per CONVENTIONS.md §Query helpers: Extend shared query infrastructure in `common/src/db/query.rs` for reuse across modules.
Applies: task modifies `common/src/db/query.rs` matching the shared query helper convention.

Per CONVENTIONS.md §Error handling: All new service methods must return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the error handling convention.

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (text match quality) by default
- [ ] Exact matches on identifiers rank higher than partial text matches (note: based on assumption about desired ranking behavior, pending clarification on relevance definition)
- [ ] Search continues to return results across all entity types (SBOMs, advisories, packages)
- [ ] The existing search API contract is preserved — response shape remains `PaginatedResults<T>` (note: pending clarification on whether the response schema must be strictly identical)
- [ ] New query helpers in `common/src/db/query.rs` are reusable by other modules

## Test Requirements
- [ ] Unit test: relevance ranking orders exact matches above partial matches
- [ ] Unit test: search with no results returns empty paginated response
- [ ] Integration test: full-text search returns ranked results from PostgreSQL

## Dependencies
- Depends on: Task 1 — search-index-migration (GIN indexes must exist for efficient full-text search)

[sdlc-workflow] Description digest: sha256-md:7b4244f1889c7f15d37b62f55263321130f4f734749035b7c23ba5f80594f1e3
