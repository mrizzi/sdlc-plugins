# Task 3 — Add Filter Parameters to Search Endpoint

## Repository
trustify-backend

## Description
Add filtering capabilities to the search endpoint so users can narrow search results by entity type, severity, and date range. This addresses the "add filters" requirement. The filters are applied as query parameters on the existing `GET /api/v2/search` endpoint and are combined with the full-text search query using AND logic. The implementation uses the shared query builder infrastructure in `common/` to ensure consistency with filtering patterns across other endpoints.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend SearchService search method to accept and apply filter parameters (entity type, severity, date range)
- `modules/search/src/endpoints/mod.rs` — add filter query parameter deserialization to the `GET /api/v2/search` handler; validate filter values
- `common/src/db/query.rs` — add shared filter helpers for entity type discrimination, severity filtering, and date range filtering if not already present

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional): filter by entity type (`sbom`, `advisory`, `package`)
  - `severity` (string, optional): filter advisories by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - `date_from` (ISO 8601 date, optional): filter results created/modified on or after this date
  - `date_to` (ISO 8601 date, optional): filter results created/modified on or before this date

## Implementation Notes
- The search endpoint at `modules/search/src/endpoints/mod.rs` currently handles `GET /api/v2/search`. Add an Axum `Query<SearchFilters>` extractor struct with optional fields for each filter parameter.
- In `SearchService`, apply filters as additional WHERE clauses on the search query. Entity type filtering should select from specific entity tables rather than searching all tables. Severity filtering applies only to advisory entities (via the `severity` field in `AdvisorySummary`). Date range filtering applies to all entity types using their created/modified timestamps.
- Use `common/src/db/query.rs` shared helpers for pagination and sorting. If the existing helpers don't support date range or enum filtering, extend them with reusable methods.
- Validate filter parameter values: return a 400 Bad Request with a descriptive error message for invalid entity types, severity values, or malformed dates.
- Follow the existing endpoint pattern: use `PaginatedResults<T>` from `common/src/model/paginated.rs` for response wrapping.
- Follow the error handling pattern: `Result<T, AppError>` with `.context()` wrapping as seen across all endpoint handlers.
- Per `docs/constraints.md` section 2 (Commit Rules): commit must reference TC-9002 and follow Conventional Commits.
- Per `docs/constraints.md` section 5.4: reuse existing query helper patterns rather than duplicating filter logic.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; extend for new filter types
- `common/src/model/paginated.rs` — PaginatedResults wrapper for paginated responses
- `common/src/error.rs` — AppError enum for validation error responses
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct contains the `severity` field referenced by the severity filter
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of a list endpoint with query parameter extraction; follow the same pattern for filter parameter deserialization
- `modules/fundamental/src/advisory/endpoints/list.rs` — example of advisory list endpoint pattern

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Multiple filters can be combined (e.g., `entity_type=advisory&severity=high`)
- [ ] Filters work correctly in combination with search query text
- [ ] Invalid filter values return 400 Bad Request with descriptive error messages
- [ ] Pagination works correctly with active filters

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` filter, verify only SBOMs returned
- [ ] Integration test: search with `entity_type=advisory` filter, verify only advisories returned
- [ ] Integration test: search with `severity=critical` filter, verify only matching advisories returned
- [ ] Integration test: search with date range filter, verify only results within range returned
- [ ] Integration test: combine multiple filters, verify AND logic applied correctly
- [ ] Integration test: invalid filter values return 400 status code
- [ ] Integration test: filters combined with full-text search query return correct filtered and ranked results

## Dependencies
- Depends on: Task 2 — Enhance SearchService with Relevance-Based Ranking
