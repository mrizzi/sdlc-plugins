## Repository
trustify-backend

## Description
Add filter query parameters to the `GET /api/v2/search` endpoint: `entity_type`, `severity`, `date_from`, and `date_to`. Filters combine with AND logic to allow users to narrow search results.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add query parameter extraction for filter fields
- `modules/search/src/service/mod.rs` — add filter logic to search queries, applying filters before full-text search ranking

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query params `?entity_type=advisory|sbom|package`, `?severity=critical|high|medium|low`, `?date_from=YYYY-MM-DD`, `?date_to=YYYY-MM-DD`. Multiple filters combine with AND logic.

## Implementation Notes
- Define a `SearchFilters` query parameter struct with optional fields for each filter, using Axum's `Query<T>` extractor. Follow the pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter extraction.
- Apply filters in `SearchService` before the full-text search ranking to reduce the result set early. Use SeaORM `.filter()` conditions following patterns in `common/src/db/query.rs`.
- `entity_type` filter limits results to a single entity type (advisory, sbom, or package).
- `severity` filter only applies to advisory results (ignore for other entity types).
- `date_from`/`date_to` filter by creation or modification date.
- **Assumption pending clarification**: using AND combination logic for multiple filters, since the feature does not specify how filters interact. Entity type, severity, date_from, and date_to are assumed as the most useful filter dimensions based on the existing data model.

## Reuse Candidates
- `modules/search/src/endpoints/mod.rs` — existing search endpoint handler
- `modules/search/src/service/mod.rs::SearchService` — search service where filter logic is added
- `common/src/db/query.rs` — shared query builder helpers for filtering
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for query parameter extraction pattern

## Acceptance Criteria
- [ ] `entity_type` filter limits results to the specified entity type
- [ ] `severity` filter limits advisory results to the specified severity level
- [ ] `date_from` and `date_to` filter results by date range
- [ ] Multiple filters combine with AND logic
- [ ] Existing search behavior without filters is unchanged

## Test Requirements
- [ ] Integration test: filter by entity_type returns only results of that type
- [ ] Integration test: filter by severity returns only advisories with matching severity
- [ ] Integration test: date range filter returns only results within the range
- [ ] Integration test: combining multiple filters narrows results correctly
- [ ] Integration test: search without filters returns same results as before (regression)

## Dependencies
- Depends on: Task 2 — Search relevance scoring (filters should work with the new ranking)
