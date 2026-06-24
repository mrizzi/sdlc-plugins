## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the SearchService to use PostgreSQL full-text search with relevance ranking via `ts_rank`. This addresses TC-9002 requirement: "Results should be more relevant." Currently the search likely uses basic pattern matching; this task replaces that with proper full-text search queries using the tsvector indexes created in Task 1, and orders results by relevance score.

**AMBIGUITY flagged**: "Relevant results" is undefined in the feature. **ASSUMPTION pending clarification**: Relevance is defined as PostgreSQL `ts_rank` score based on text match quality against the user's search query. Results are ordered by this score descending by default. Users can optionally override with explicit sort parameters (e.g., by date or severity).

## Files to Modify
- `modules/search/src/service/mod.rs` — Rewrite the core search logic in `SearchService` to use `to_tsquery()` against the `search_vector` columns and rank results with `ts_rank()`. Add support for an optional `sort` parameter (relevance, date, severity).
- `common/src/db/query.rs` — Add a shared `full_text_search` query builder helper that constructs the tsquery, joins results across entity tables, and applies ts_rank ordering. This helper will be reusable by list endpoints in the future.

## Implementation Notes
The `SearchService` in `modules/search/src/service/mod.rs` currently provides full-text search across entities. Modify it to:

1. Parse the user's search query into a `tsquery` using `plainto_tsquery('english', $1)` for natural language input or `to_tsquery()` for advanced syntax
2. Query each entity table's `search_vector` column using the `@@` operator
3. Compute `ts_rank(search_vector, query)` for each matching row
4. Union results across sbom, advisory, and package tables with a `type` discriminator
5. Order by ts_rank descending by default
6. Return results wrapped in `PaginatedResults<T>` as required by existing response conventions

The shared query helper in `common/src/db/query.rs` should follow the existing patterns for filtering, pagination, and sorting already present in that file.

Per Key Conventions (Response types): List/search results must return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's endpoint response scope.

Per Key Conventions (Query helpers): Shared filtering, pagination, and sorting logic belongs in `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per Key Conventions (Error handling): All service methods should return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`@@` operator with tsquery)
- [ ] Results are ranked by `ts_rank` score by default
- [ ] Search spans sbom, advisory, and package entities
- [ ] Results include a relevance score in the response
- [ ] Optional sort parameter allows overriding default relevance ordering
- [ ] Backward compatibility: existing search queries continue to return results (new ranking may change order but not omit valid matches)
- [ ] Paginated results use `PaginatedResults<T>` wrapper

## Test Requirements
- [ ] Searching for a known term returns matching entities ranked by relevance
- [ ] A more specific query returns a higher-ranked result than a less specific one
- [ ] Empty search query returns a meaningful default (e.g., most recent items)
- [ ] Sort parameter correctly overrides default relevance ordering
- [ ] Pagination works correctly with ranked results

## Dependencies
- Depends on: Task 1 — Search indexes migration (requires tsvector columns and GIN indexes to be present)

## API Changes
- `GET /api/v2/search` now supports an optional `sort` query parameter with values: `relevance` (default), `date`, `severity`
- Response objects include a `relevance_score` field (float) when sorted by relevance

[sdlc-workflow] Description digest: sha256-md:f1310ec6325fd4b0b363090e6120d9f5cc364ae7eecba04991b38297334bed4b
