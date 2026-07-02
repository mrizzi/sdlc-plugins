additional_fields: { "labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": ["RHTPA 1.6.0"] }

## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results so that the most pertinent results appear first. The feature description states "Users complain about irrelevant results" but does not define what constitutes a "relevant" result or specify a ranking algorithm.

**Assumption (pending clarification):** "More relevant results" is interpreted as implementing PostgreSQL `ts_rank` or `ts_rank_cd` scoring on the full-text search tsvector columns, ordering results by descending relevance score. The ranking will weight exact matches higher than partial matches. If domain-specific ranking signals are needed (e.g., recency, advisory severity, SBOM completeness), those would require further clarification from the product owner.

**Ambiguity:** The feature does not define relevance criteria. It is unclear whether relevance means text-match quality alone, or should incorporate domain signals such as advisory severity, SBOM age, or package popularity. This task implements text-match relevance ranking; domain-specific boosting would require a follow-up specification.

## Files to Modify
- `modules/search/src/service/mod.rs` -- Add ts_rank scoring to the full-text search query; order results by relevance score descending
- `modules/search/src/endpoints/mod.rs` -- Accept an optional `sort` query parameter allowing users to choose between relevance-ranked and date-sorted results

## Implementation Notes
- Build on the full-text search implementation from Task 1 (search performance indexes). The tsvector/tsquery infrastructure must be in place before relevance ranking can be applied.
- In `modules/search/src/service/mod.rs`, use PostgreSQL's `ts_rank(tsvector_column, query)` function to compute a relevance score for each result row. Add this as a computed column in the SELECT and use it for ORDER BY.
- Expose an optional `sort` query parameter on the `GET /api/v2/search` endpoint in `modules/search/src/endpoints/mod.rs`. Default to relevance ranking when a search query is present; allow `sort=date` as an alternative.
- Use the existing sorting helpers in `common/src/db/query.rs` to integrate the new sort option consistently with other list endpoints.
- Return results using `PaginatedResults<T>` from `common/src/model/paginated.rs` to maintain consistency with all other list endpoints in the codebase.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping.
- Per CONVENTIONS.md: use the shared query builder helpers from `common/src/db/query.rs` for sorting integration.
  Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared sorting helpers; extend or reuse for relevance-based sort option
- `common/src/model/paginated.rs::PaginatedResults` -- Response wrapper for paginated list results; continue using for search responses
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Reference implementation for list endpoints with sorting and pagination; follow the same pattern

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest first) by default when a search query term is provided
- [ ] An optional `sort` query parameter is accepted on `GET /api/v2/search` (values: `relevance`, `date`)
- [ ] Results for a specific search term rank exact matches above partial matches
- [ ] Pagination continues to work correctly with relevance-ranked results
- [ ] When no search query is provided (empty search), results fall back to date-based ordering

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying that a search for a known term returns results with exact matches ranked before partial matches
- [ ] Integration test verifying the `sort=date` parameter overrides relevance ranking
- [ ] Integration test verifying default sort behavior (relevance) when `sort` parameter is omitted

## Dependencies
- Depends on: Task 1 -- Add database indexes for search performance optimization (requires tsvector/tsquery infrastructure)
