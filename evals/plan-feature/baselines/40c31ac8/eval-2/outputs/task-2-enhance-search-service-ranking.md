## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the SearchService to use PostgreSQL full-text search primitives (tsvector/tsquery) with ts_rank-based relevance ordering. This addresses the "results should be more relevant" requirement by replacing basic text matching with ranked full-text search.

**Ambiguity note:** The feature specifies "results should be more relevant" without defining relevance criteria, providing examples of irrelevant results, or specifying a ranking algorithm. **Assumption pending clarification:** We assume PostgreSQL `ts_rank()` with default weights provides adequate relevance ranking. The ranking weights across entity types (SBOM, advisory, package) are unspecified; we assume equal weighting initially. Stakeholders should review search result quality after implementation and provide feedback on ranking adjustments.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor SearchService to use `to_tsquery()` for query parsing and `ts_rank()` for result ordering against the `search_vector` columns added in Task 1

## Implementation Notes
Modify the existing `SearchService` in `modules/search/src/service/mod.rs` to:

1. Parse user search input into a tsquery using `plainto_tsquery('english', ...)` for natural-language queries or `to_tsquery('english', ...)` for advanced syntax
2. Match against the `search_vector` columns on `sbom`, `advisory`, and `package` tables using the `@@` operator
3. Order results by `ts_rank(search_vector, query)` descending so the most relevant results appear first
4. Continue returning results via `PaginatedResults<T>` from `common/src/model/paginated.rs`

Use the existing pagination and sorting infrastructure in `common/src/db/query.rs` as the foundation, extending it to support ts_rank-based ordering.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all database query operations in the service. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `common/src/db/query.rs::` — Shared query builder helpers for filtering, pagination, and sorting; extend these for full-text search ordering rather than building a separate query mechanism
- `common/src/model/paginated.rs::PaginatedResults` — Continue using this response wrapper for paginated search results
- `common/src/error.rs::AppError` — Use for error handling with `.context()` wrapping

## Acceptance Criteria
- [ ] Search queries use PostgreSQL tsvector/tsquery matching instead of basic text comparison
- [ ] Search results are ordered by relevance score (ts_rank) descending
- [ ] Search covers SBOM, advisory, and package entities
- [ ] Natural-language search queries are handled correctly (multi-word queries, common terms)
- [ ] Empty or whitespace-only queries return an appropriate error or empty result set
- [ ] Pagination continues to work correctly with relevance-ordered results

## Test Requirements
- [ ] Verify that a search for a known term returns the expected entity as the top result
- [ ] Verify that multi-word queries return results matching all terms ranked higher than partial matches
- [ ] Verify that pagination parameters (limit, offset) work correctly with ranked results
- [ ] Verify that an empty query returns an appropriate response

## Dependencies
- Depends on: Task 1 — Add database migration for full-text search indexes

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0
- labels: ai-generated-jira
