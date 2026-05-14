# Task 2 — Implement ranked full-text search in SearchService

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the `SearchService` to use PostgreSQL full-text search with ranking instead of basic pattern matching. Search results should be scored by relevance using `ts_rank` (or equivalent) and returned in descending relevance order. The service should search across multiple entity types (SBOMs, advisories, packages) and return unified, ranked results.

**Ambiguity note:** The feature description states "results should be more relevant" without defining relevance criteria. This task interprets relevance as PostgreSQL full-text search ranking (`ts_rank`), which scores results based on term frequency and proximity. If a more sophisticated ranking algorithm is needed (e.g., incorporating recency, popularity, or domain-specific weights), it should be specified in a follow-up requirement.

## Files to Modify
- `modules/search/src/service/mod.rs` — Extend `SearchService` to use PostgreSQL full-text search with `ts_rank` scoring, searching across SBOM, advisory, and package entities
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` endpoint handler to pass-through ranking parameters and return results with relevance scores

## API Changes
- `GET /api/v2/search` — MODIFY: Response now includes a `score` field per result indicating relevance rank. Results are ordered by descending relevance score by default.

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` provides full-text search across entities. Extend it to use PostgreSQL `to_tsquery` and `ts_rank` for ranked results rather than simple `LIKE` or `ILIKE` queries.
- Use the query builder helpers in `common/src/db/query.rs` for constructing the search queries. These helpers already support filtering, pagination, and sorting — extend or compose with them for the ranked search query.
- Return results using `PaginatedResults<T>` from `common/src/model/paginated.rs` to maintain consistency with other list endpoints.
- Search should query across the SBOM entity (`entity/src/sbom.rs`), advisory entity (`entity/src/advisory.rs`), and package entity (`entity/src/package.rs`).
- Follow the error handling pattern used throughout the codebase: return `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs`).
- The search result type should include: entity type identifier, entity ID, display name/title, relevance score, and a summary snippet if feasible.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting that should be composed with the new ranked search query
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper to use for search results
- `common/src/error.rs` — `AppError` enum for consistent error handling
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` search method as a reference for existing search patterns in the codebase

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL full-text search (`to_tsquery` / `ts_rank`) for query execution
- [ ] Search results are ranked by relevance score in descending order
- [ ] Search queries span SBOM, advisory, and package entities
- [ ] Each result includes an entity type identifier, entity ID, display name, and relevance score
- [ ] The `GET /api/v2/search` endpoint returns ranked results with score metadata
- [ ] Existing search functionality is not broken — queries that worked before continue to return results

## Test Requirements
- [ ] Unit or integration test verifying that search results are ordered by relevance (a more specific query term ranks higher than a partial match)
- [ ] Test verifying that search spans all three entity types (SBOM, advisory, package)
- [ ] Test verifying that empty search queries return an appropriate response (empty results or validation error)
- [ ] Test verifying that search results include relevance score and entity type metadata

## Dependencies
- Depends on: Task 1 — Add full-text search indexes migration
