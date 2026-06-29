## Repository
trustify-backend

## Target Branch
main

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": ["RHTPA 1.6.0"]}

## Description
Implement relevance-scored search ranking in the SearchService to replace the current unranked search results. Users have reported that search "doesn't return useful results," so this task introduces weighted full-text ranking using PostgreSQL's `ts_rank` function to prioritize more relevant matches.

**Assumption (pending clarification):** No relevance ranking criteria were specified in the feature description. This implementation assumes name/title matches should rank higher than description matches. The exact field weights (e.g., name weight 1.0 vs. description weight 0.4) are assumptions that need product owner validation. The response shape adds a `score` field but does not remove or rename any existing fields (backward-compatible).

## Files to Modify
- `modules/search/src/service/mod.rs` — Modify `SearchService` to use `ts_rank` for scoring and `to_tsquery` for query parsing instead of simple `LIKE`/`ILIKE` patterns. Add weighted ranking across entity fields.
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` handler to accept an optional `sort_by=relevance` query parameter and pass it to the service layer. Default sort order should be by relevance score descending.
- `common/src/db/query.rs` — Add a `search_rank` helper function that constructs `ts_rank` expressions, following the pattern of existing query builder helpers for filtering and sorting.

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional `sort_by` query parameter (values: `relevance`, `name`, `date`; default: `relevance`). Response items gain an optional `score` float field indicating relevance rank.

## Implementation Notes
- In `modules/search/src/service/mod.rs`, the existing `SearchService` provides full-text search across entities. Replace any `LIKE '%query%'` patterns with `to_tsvector('english', column) @@ to_tsquery('english', query)` and rank with `ts_rank`.
- Use the `common/src/db/query.rs` query builder helpers as the base for the new `search_rank` helper. Follow the existing patterns for constructing SeaORM expressions.
- Results must continue to return `PaginatedResults<T>` from `common/src/model/paginated.rs` — add the `score` field to the search result item type, not replace the pagination wrapper.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers for filtering, pagination, and sorting. The new `search_rank` helper should follow the same patterns.
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper for list endpoints. Search results must use this wrapper.

## Acceptance Criteria
- [ ] Search results are ranked by relevance score by default (most relevant first)
- [ ] Name/title matches rank higher than description-only matches
- [ ] The `sort_by` query parameter allows switching between relevance, name, and date sorting
- [ ] Response includes a `score` field for each result item when sorted by relevance
- [ ] API change is backward-compatible — existing clients without `sort_by` parameter get relevance-sorted results
- [ ] Empty queries return results in a sensible default order (e.g., most recent)

## Test Requirements
- [ ] Integration test: search for a known entity name returns it as the top result
- [ ] Integration test: name match ranks higher than description-only match
- [ ] Integration test: `sort_by=relevance` and `sort_by=name` produce different orderings
- [ ] Integration test: empty search query returns results without error
- [ ] Integration test: special characters in search query are handled safely (no SQL injection, no panics)

## Dependencies
- Depends on: Task 1 — Add database indexes for full-text search optimization (indexes must exist for `ts_rank` to be efficient)

[sdlc-workflow] Description digest: sha256-md:81ff9718badf6a45d80e38a2ed37a5f8520cf99eb184e5e480f3675b44d5a9d6
