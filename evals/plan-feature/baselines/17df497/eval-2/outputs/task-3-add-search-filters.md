# Task 3 — Add filter parameters to the search endpoint

## Repository
trustify-backend

## Description
Extend the `GET /api/v2/search` endpoint to accept filter parameters, enabling users to
narrow search results by entity type, date range, and severity (for advisories). This
addresses the MVP requirement "Add filters — some kind of filtering capability." The
filters must integrate with the full-text search from Task 2 so that filtering and
relevance ranking work together.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter
  parameters: `entity_type` (enum: sbom, advisory, package), `date_from` (ISO 8601),
  `date_to` (ISO 8601), `severity` (enum matching advisory severity values)
- `modules/search/src/service/mod.rs` — Extend `SearchService` search method to accept
  filter parameters and apply them as `WHERE` clause conditions alongside the full-text
  search query
- `modules/search/src/lib.rs` — Add filter parameter struct/types if needed

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional): Filter by entity type — `sbom`, `advisory`, or `package`
  - `date_from` (string, optional): ISO 8601 date — return only entities created/modified on or after this date
  - `date_to` (string, optional): ISO 8601 date — return only entities created/modified on or before this date
  - `severity` (string, optional): Filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)

## Implementation Notes
- Inspect the existing endpoint handler in `modules/search/src/endpoints/mod.rs` to
  understand the current query parameter extraction pattern. Follow the same Axum
  `Query<T>` extractor approach.
- Define a `SearchFilters` struct with optional fields for each filter parameter.
  Use `Option<T>` for all filter fields so they are all optional.
- The `entity_type` filter should control which entity tables are queried. When set to
  `sbom`, only search the `sbom` table; when set to `advisory`, only search the `advisory`
  table; when set to `package`, only search the `package` table. When omitted, search all
  tables (current behavior).
- The `severity` filter only applies when searching advisories. If `entity_type` is set
  to `sbom` or `package`, the `severity` filter should be ignored (or return a validation
  error — follow the pattern established by other endpoints).
- The `date_from` and `date_to` filters should apply to the entity creation or modification
  timestamp. Inspect entity definitions in `entity/src/` to identify the correct timestamp
  column names.
- Reuse the filtering helpers in `common/src/db/query.rs` for constructing filter
  conditions. These helpers already support filtering and pagination patterns.
- Per constraints §5.4: extend existing query helpers rather than building parallel
  filtering infrastructure.
- Follow the error handling pattern from `common/src/error.rs` — return `AppError` for
  invalid filter values (e.g., malformed dates, unknown entity types).

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers already support filtering
  and pagination. Extend these to support the new search-specific filter parameters.
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct
  includes a severity field. Reference this for valid severity values.
- `common/src/error.rs` — `AppError` enum for validation error responses.

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` filters by date range
- [ ] `GET /api/v2/search?severity=critical` filters advisory results by severity
- [ ] Filters combine with full-text search query (e.g., `?q=openssl&entity_type=advisory&severity=high`)
- [ ] Invalid filter values return appropriate error responses
- [ ] Omitting all filters preserves current behavior (search all entities)

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOMs
- [ ] Integration test: search with `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Integration test: search with `date_from` and `date_to` returns only entities in range
- [ ] Integration test: search combining text query and filters returns correct filtered results
- [ ] Integration test: invalid `entity_type` value returns 400 Bad Request
- [ ] Integration test: `severity` filter is ignored or errors when `entity_type` is not `advisory`

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use full-text search with relevance ranking
