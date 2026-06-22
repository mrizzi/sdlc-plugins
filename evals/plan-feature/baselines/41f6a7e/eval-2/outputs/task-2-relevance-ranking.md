# Task 2: Enhance SearchService with relevance ranking

## Repository

trustify-backend

## Target Branch

`main`

## Description

Replace the existing LIKE/ILIKE pattern-matching search in `SearchService` with PostgreSQL full-text search using `tsvector`/`tsquery` and `ts_rank` for relevance scoring. Search results will be ordered by relevance rank by default, with the rank score included in the response so clients can display or use it.

## Files to Modify

- `modules/search/src/service/mod.rs` -- Refactor the search method to:
  - Parse the user's query string into a `tsquery` using `plainto_tsquery('english', $1)` or `websearch_to_tsquery('english', $1)` for more natural query syntax
  - Match against the `search_vector` column added by Task 1 instead of using `LIKE`/`ILIKE`
  - Compute relevance score using `ts_rank(search_vector, query)` or `ts_rank_cd` for proximity-aware ranking
  - Order results by relevance score descending by default
  - Fall back to ILIKE for very short queries (1-2 characters) where full-text search is less effective
  - Return the relevance score in the result payload

- `modules/search/src/endpoints/mod.rs` -- Update the GET `/api/v2/search` handler to:
  - Accept an optional `sort_by` query parameter (values: `relevance`, `date`, `name`) defaulting to `relevance`
  - Pass sort preference through to the service layer

## API Changes

**GET /api/v2/search**

New query parameter:
- `sort_by` (optional, string): One of `relevance` (default), `date`, `name`. Controls result ordering.

Response body change -- each search result item gains a new field:
- `relevance_score` (float, 0.0-1.0): PostgreSQL ts_rank score normalized to [0,1]. Present only when `sort_by=relevance` or omitted.

This is a backward-compatible addition; no existing fields are removed or renamed.

## Reuse Candidates

- `common/src/db/query.rs` -- Reuse existing sorting and pagination helpers. May need to extend the `Sorting` enum or add a `RelevanceSort` variant to support ordering by ts_rank.
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` continues to wrap the response. The individual item type gains the `relevance_score` field.

## Implementation Notes

- Use SeaORM's `Statement::from_sql_and_values` or raw query fragments for the `ts_rank` and `tsquery` operations since SeaORM does not have built-in support for these PostgreSQL functions.
- The query construction pattern should mirror how `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` builds its search queries -- check that file for conventions on combining service-layer queries with raw SQL fragments.
- Normalize the ts_rank score to [0,1] by dividing by the maximum rank in the result set, or use `ts_rank(...) / (1 + ts_rank(...))` for a bounded score.
- Handle empty query strings gracefully: return an empty result set rather than matching everything.
- For the ILIKE fallback on short queries, preserve the existing behavior so single-character searches still work.
- Ensure the `tsquery` is sanitized to prevent syntax errors from special characters in user input. `plainto_tsquery` handles this automatically; `to_tsquery` does not.

## Acceptance Criteria

- [ ] Search results are ranked by relevance when using multi-word queries
- [ ] A search for "critical vulnerability openssl" returns advisories mentioning those terms ranked higher than partial matches
- [ ] The `relevance_score` field is present in search result items
- [ ] The `sort_by` parameter works for all three values (`relevance`, `date`, `name`)
- [ ] Empty query strings return an empty result set with 200 status
- [ ] Special characters in query strings do not cause 500 errors
- [ ] Short queries (1-2 chars) still return results via ILIKE fallback
- [ ] Existing search API consumers are not broken (backward compatible)

## Test Requirements

- Unit test: verify tsquery construction from various input strings (normal, empty, special chars, single char)
- Integration test: insert test data with known content, search for specific terms, and assert ordering by relevance
- Integration test: verify `sort_by` parameter changes result ordering
- Integration test: verify backward compatibility -- existing search requests without `sort_by` still work

## Dependencies

- Task 1 (search indexes) must be completed first -- the `search_vector` columns and GIN indexes must exist
