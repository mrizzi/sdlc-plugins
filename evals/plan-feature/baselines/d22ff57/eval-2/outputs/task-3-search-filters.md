# Task 3 — Add filter parameters to the search endpoint

## Repository
trustify-backend

## Description
Extend the `GET /api/v2/search` endpoint to accept optional filter query parameters,
enabling users to narrow search results by entity type, date range, and severity level.
This addresses the MVP requirement "Add filters — some kind of filtering capability."
Filters must integrate with the full-text search and relevance ranking from Task 2
so that filtering and ranked search work together seamlessly.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter
  parameters using an Axum `Query<SearchFilters>` extractor: `entity_type` (enum: sbom,
  advisory, package), `date_from` (ISO 8601 date string), `date_to` (ISO 8601 date string),
  `severity` (string matching advisory severity values)
- `modules/search/src/service/mod.rs` — Extend `SearchService` search method to accept
  a `SearchFilters` struct and apply filter conditions as additional `WHERE` clauses
  alongside the full-text search query
- `modules/search/src/lib.rs` — Export new filter types if needed

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional): Filter results to a single entity type — `sbom`, `advisory`, or `package`
  - `date_from` (string, optional): ISO 8601 date — return only entities created/modified on or after this date
  - `date_to` (string, optional): ISO 8601 date — return only entities created/modified on or before this date
  - `severity` (string, optional): Filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)

## Implementation Notes
- Inspect the existing endpoint handler in `modules/search/src/endpoints/mod.rs` to
  understand the current query parameter extraction pattern. Follow the same Axum
  `Query<T>` extractor approach used by other endpoints.
- Define a `SearchFilters` struct with optional fields (`Option<T>`) for each filter
  parameter. Place it in `modules/search/src/endpoints/mod.rs` or in a dedicated types
  file within the module, following the pattern used by other modules.
- The `entity_type` filter controls which entity tables are queried:
  - When set to `sbom`, only search the `sbom` table
  - When set to `advisory`, only search the `advisory` table
  - When set to `package`, only search the `package` table
  - When omitted, search all tables (preserving current default behavior)
- The `severity` filter applies only to advisory results. If `entity_type` is set to
  `sbom` or `package`, the `severity` filter should be ignored. Reference the severity
  field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` for
  valid severity values.
- The `date_from` and `date_to` filters apply to entity creation or modification timestamps.
  Inspect entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and
  `entity/src/package.rs` to identify the correct timestamp column names.
- Reuse the shared filtering helpers in `common/src/db/query.rs` for constructing filter
  conditions. These already support filtering and pagination patterns — extend them for
  search-specific filters rather than building parallel infrastructure.
- Return `AppError` from `common/src/error.rs` for invalid filter values (malformed dates,
  unknown entity types, unknown severity values).
- Per constraints §5.4: extend existing query helpers rather than duplicating filtering logic.
- Per constraints §5.2: inspect existing code before modifying.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination.
  Extend these to support search-specific filter parameters.
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` includes a
  severity field. Reference for valid severity enum values.
- `common/src/error.rs` — `AppError` enum for validation error responses.
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of list endpoint with
  query parameter extraction. Follow the same extractor pattern.

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only entities within the date range
- [ ] `GET /api/v2/search?severity=critical` filters advisory results by severity
- [ ] Filters combine correctly with full-text search (e.g., `?q=openssl&entity_type=advisory&severity=high`)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Omitting all filters preserves current behavior (search all entities)

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOMs
- [ ] Integration test: search with `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Integration test: search with `date_from` and `date_to` returns only entities within the specified range
- [ ] Integration test: combined text query and filters return correct filtered, ranked results
- [ ] Integration test: invalid `entity_type` value returns 400 Bad Request
- [ ] Integration test: `severity` filter is ignored when `entity_type` is not `advisory`

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use full-text search with relevance ranking
