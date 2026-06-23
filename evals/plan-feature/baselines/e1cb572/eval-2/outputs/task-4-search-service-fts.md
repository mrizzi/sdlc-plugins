# Task 4: Implement Full-Text Search with Relevance Ranking in SearchService

## Repository
trustify-backend

## Target Branch
main

## Description
Rewrite the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search instead of any existing naive text matching (e.g., `LIKE`/`ILIKE`). The service will leverage the FTS helpers added in Task 3 and the database indexes from Task 1 to provide fast, relevance-ranked search results across SBOMs, advisories, and packages.

**Ambiguity note:** The feature does not specify whether search should be a unified cross-entity search or per-entity. This task assumes the existing unified `SearchService` pattern is maintained, searching across all entity types and returning mixed results ranked by relevance (pending clarification).

## Files to Modify
- `modules/search/src/service/mod.rs` — Rewrite the search query logic to use `apply_fts_filter` and `apply_fts_ranking` from `common/src/db/query.rs`. Replace any `LIKE`/`ILIKE` queries with `tsvector @@ tsquery` operations. Ensure results are ordered by `ts_rank` score descending.

## Implementation Notes
- The current `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Replace the query construction with calls to the helpers from `common/src/db/query.rs` (added in Task 3).
- The search flow should be:
  1. Parse the user's search query using `parse_search_query` from `common/src/db/query.rs`
  2. Query each entity table (sbom, advisory, package) using `apply_fts_filter` to match against `search_vector`
  3. Apply `apply_fts_ranking` to order results by relevance score
  4. Combine results across entity types, maintaining relevance ordering
  5. Return results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Use the existing error handling pattern: return `Result<T, AppError>` and use `.context()` for error wrapping, as established in `common/src/error.rs`.
- If the search query is empty, return an empty result set rather than all records.
- Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — FTS helpers (`apply_fts_filter`, `apply_fts_ranking`, `parse_search_query`) added in Task 3
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper for paginated search results
- `common/src/error.rs::AppError` — Error type for consistent error handling
- `modules/fundamental/src/advisory/service/advisory.rs` — Reference for how other services query entities with filtering

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsvector @@ tsquery`) instead of `LIKE`/`ILIKE`
- [ ] Results are ranked by relevance score (`ts_rank`) in descending order
- [ ] Search works across all three entity types: SBOM, Advisory, Package
- [ ] Empty search queries return an empty result set
- [ ] Results are wrapped in `PaginatedResults<T>`
- [ ] Error handling follows the `Result<T, AppError>` pattern

## Test Requirements
- [ ] Integration test: search for a known term returns matching results ranked by relevance
- [ ] Integration test: search for a non-existent term returns empty results
- [ ] Integration test: empty search query returns empty results
- [ ] Integration test: search returns results from multiple entity types

## Dependencies
- Depends on: Task 1 — Add database migration for full-text search indexes
- Depends on: Task 2 — Update entities with search vector columns
- Depends on: Task 3 — Extend query builder with full-text search helpers

---

`[sdlc-workflow] Description digest: sha256-md:d5f9a3b7c2e84d0f1a6b3c8e7d9f2a4b6c8e0a2d4f6b8c1e3a5d7f9b0c2e4a6`
