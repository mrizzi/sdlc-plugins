## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the search endpoint (GET /api/v2/search) so users can narrow search results by entity type, severity, and date range. This addresses the "add filters" requirement.

**Ambiguity note:** The feature specifies "add filters" and "some kind of filtering capability" without defining which fields should be filterable, what filter types to support (exact match, range, multi-select), or how filters combine (AND vs OR). **Assumption pending clarification:** We assume the following initial filter set based on the existing entity models:
- `type` — filter by entity type (sbom, advisory, package) — exact match, multi-select
- `severity` — filter by advisory severity — exact match (leverages `severity` field on `AdvisorySummary`)
- `from` / `to` — filter by date range — range filter on creation/publication date

All filters combine with AND semantics. Stakeholders should confirm whether additional filter fields are needed.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter parsing for filter fields (type, severity, from, to) on the GET /api/v2/search endpoint
- `modules/search/src/service/mod.rs` — Extend SearchService to accept and apply filter parameters when building the search query

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `type` (string, comma-separated), `severity` (string), `from` (ISO 8601 date), `to` (ISO 8601 date) for filtering search results

## Implementation Notes
For the endpoint layer (`modules/search/src/endpoints/mod.rs`):
1. Define a `SearchFilterParams` struct with optional fields for `type`, `severity`, `from`, and `to`
2. Deserialize from query parameters using Axum's `Query<SearchFilterParams>` extractor
3. Pass the filter params to the SearchService

For the service layer (`modules/search/src/service/mod.rs`):
1. Accept the filter parameters in the search method
2. Build WHERE clauses conditionally based on which filters are present
3. Use the shared query helpers in `common/src/db/query.rs` for constructing filter predicates, following the existing patterns for filtering and pagination
4. The `type` filter should restrict which entity tables are queried (e.g., if `type=advisory`, only search the advisory table)
5. The `severity` filter should match against the `severity` field on the advisory entity (`entity/src/advisory.rs`)
6. The `from`/`to` filters should apply as a date range on the entity creation/publication timestamp

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for parameter validation and query execution. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` service file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers; reuse the existing filtering infrastructure rather than building custom filter logic
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field; reference this for the severity filter values
- `common/src/model/paginated.rs::PaginatedResults` — Continue using for paginated, filtered results

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `type` parameter to filter by entity type
- [ ] GET /api/v2/search accepts optional `severity` parameter to filter advisories by severity
- [ ] GET /api/v2/search accepts optional `from` and `to` parameters for date range filtering
- [ ] Filters combine with AND semantics (all specified filters must match)
- [ ] Omitting a filter parameter means no restriction on that dimension
- [ ] Invalid filter values return a clear error response with appropriate HTTP status
- [ ] Filtering works correctly in combination with full-text search ranking from Task 2

## Test Requirements
- [ ] Verify filtering by entity type returns only entities of the specified type
- [ ] Verify filtering by severity returns only advisories matching the severity
- [ ] Verify date range filtering returns only entities within the specified range
- [ ] Verify combining multiple filters narrows results correctly
- [ ] Verify invalid filter values return appropriate error responses
- [ ] Verify omitting all filters returns unfiltered results (backward compatibility)

## Dependencies
- Depends on: Task 2 — Enhance SearchService with full-text search ranking

## Additional Fields
- priority: Normal
- fixVersions: RHTPA 1.6.0
- labels: ai-generated-jira
