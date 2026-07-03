## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance scoring in the `SearchService` so that search results are ranked by text-match quality using PostgreSQL's `ts_rank` function. This task addresses the "results should be more relevant" requirement from TC-9002. Currently, search results are returned without ranking; after this change, results will be ordered by a computed relevance score so that the best matches appear first.

**Assumption pending clarification:** "Relevant" is interpreted as text-match relevance using PostgreSQL full-text search ranking (`ts_rank`). The feature description does not define relevance criteria, ranking algorithm, weighting preferences, or what constitutes an irrelevant result. If domain-specific relevance factors (e.g., recency, severity, popularity) are needed, additional requirements must be provided.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": "RHTPA 1.6.0" }

## Files to Modify
- `modules/search/src/service/mod.rs` -- modify the `SearchService` search method to use `tsquery` for query parsing and `ts_rank` for scoring results against the `tsvector` columns created in Task 1; add relevance score to result items and order by descending score
- `modules/search/src/endpoints/mod.rs` -- update the search endpoint response to include the relevance score field in each result item (additive change, backwards-compatible)

## API Changes
- `GET /api/v2/search` -- MODIFY: each result item in the response now includes an additional `relevance_score` field (f64). Existing fields are preserved. The results array is now ordered by descending relevance score.

## Implementation Notes
Modify the search query in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search functions:

1. Parse the user's search query into a `tsquery` using `plainto_tsquery()` or `to_tsquery()` for the search term
2. Match against the `tsvector` columns added by the migration in Task 1 using the `@@` operator
3. Compute a relevance score using `ts_rank(tsvector_column, tsquery)` for each matching row
4. Order results by `ts_rank` descending so the most relevant results appear first
5. Add the computed score to the result model as a `relevance_score: f64` field

Use SeaORM's `select_only()` with `column_as()` to include the `ts_rank` computed column in the query, similar to the aggregation pattern used in other service methods. If SeaORM does not directly support `ts_rank`, use a raw SQL expression via `Expr::cust()`.

The response type returned by the endpoint in `modules/search/src/endpoints/mod.rs` should include the new `relevance_score` field. This is an additive change -- existing fields in the response are unchanged.

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` module scope.

Per CONVENTIONS.md: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `modules/search/src/service/mod.rs::SearchService` -- existing search implementation; modify in place rather than creating a new service
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; reuse for ordering by relevance score
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper for list endpoints; ensure relevance-scored results use the same wrapper

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (most relevant first)
- [ ] Each result item includes a `relevance_score` field (f64) reflecting text-match quality
- [ ] A search query that exactly matches a title scores higher than a partial match
- [ ] Empty search queries return results in default order (no ranking applied)
- [ ] Existing search response shape is preserved (new field is additive)

## Test Requirements
- [ ] Integration test: search for an exact SBOM name returns that SBOM as the top result
- [ ] Integration test: search for a partial term returns results ordered by relevance (exact matches first, partial matches lower)
- [ ] Integration test: verify `relevance_score` field is present in the response JSON for each result item
- [ ] Integration test: existing search test cases continue to pass (backwards compatibility)

## Verification Commands
- `cargo build -p trustify-search` -- compiles without errors
- `cargo test -p trustify-search` -- unit tests pass
- `cargo test --test search` -- integration tests pass

## Dependencies
- Depends on: Task 1 -- Add full-text search indexes via database migration
