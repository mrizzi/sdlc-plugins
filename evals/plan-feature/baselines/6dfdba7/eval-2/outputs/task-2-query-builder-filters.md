## Repository
trustify-backend

## Description
Extend the shared query builder in `common/src/db/query.rs` to support full-text search ranking and structured filter parameters. This provides the foundational query infrastructure that the search service and list endpoints will use. Currently, the query builder handles filtering, pagination, and sorting; this task adds full-text search query execution with relevance scoring and a more expressive filter parameter model.

**Assumption (pending clarification):** Filter types are assumed to include equality, substring match, and date range, since the feature description only says "some kind of filtering capability" without specifying operators. The exact set of filterable fields per entity is also unspecified and assumed to be: severity (advisory), license (package), and date fields (all entities).

**Assumption (pending clarification):** Relevance scoring is assumed to use PostgreSQL's `ts_rank` function applied to the tsvector columns created in Task 1. No custom ranking algorithm or weighting scheme was specified.

## Files to Modify
- `common/src/db/query.rs` — Add full-text search query construction (tsquery building, ts_rank scoring), structured filter parameter parsing, and filter application to SeaORM query builders
- `common/src/db/mod.rs` — Export any new public types added for filter/search support
- `common/src/model/paginated.rs` — Add an optional `relevance_score` field to `PaginatedResults<T>` items or create a scored wrapper type

## Files to Create
- `common/src/db/search.rs` — Full-text search helper: tsquery construction from user input, ts_rank ordering, highlight/snippet generation utilities

## Implementation Notes
- The existing `query.rs` already provides shared query builder helpers for filtering, pagination, and sorting — extend this rather than replacing it
- For full-text search, build `tsquery` from user input using `plainto_tsquery` or `websearch_to_tsquery` (PostgreSQL 11+) for robust handling of user-typed search terms
- Ranking should use `ts_rank(search_vector, query)` and allow ordering results by relevance score descending
- Filter parameters should be parsed from query string parameters following a consistent convention, e.g., `?filter[severity]=critical&filter[date_from]=2024-01-01`
- Reference `common/src/model/paginated.rs` for the `PaginatedResults<T>` type — consider whether relevance score belongs on each item or as metadata
- Reference `common/src/error.rs` for the `AppError` enum — add a variant or use existing variants for invalid filter parameter errors

## Reuse Candidates
- `common/src/db/query.rs` — Existing filtering and pagination helpers to extend
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response wrapper to potentially extend with score information
- `common/src/error.rs::AppError` — Error type for invalid filter parameter handling

## Acceptance Criteria
- [ ] Full-text search queries can be constructed from arbitrary user input strings
- [ ] Results can be ordered by relevance score (ts_rank)
- [ ] Structured filters can be applied to SeaORM queries for at least equality, substring, and date range operations
- [ ] Invalid filter parameters produce clear error responses via AppError
- [ ] New query builder functions are composable with existing pagination and sorting helpers

## Test Requirements
- [ ] Unit tests for tsquery construction from various user inputs (single word, multiple words, special characters)
- [ ] Unit tests for filter parameter parsing and validation
- [ ] Unit tests for composing full-text search with pagination and sorting
- [ ] Test that invalid filter values return appropriate errors

## Verification Commands
- `cargo test -p common` — All common crate tests pass

## Dependencies
- Depends on: Task 1 — Add database indexes and full-text search migration (tsvector columns must exist)
