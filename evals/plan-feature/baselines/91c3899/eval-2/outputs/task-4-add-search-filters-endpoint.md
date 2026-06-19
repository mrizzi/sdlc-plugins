## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint (`GET /api/v2/search`). Users will be able to narrow search results by entity type, severity (for advisories), and date range. Filters are applied as optional query parameters and compose with the existing full-text search and pagination.

**ASSUMPTION pending clarification:** The specific filters (entity type, severity, date range) are assumed based on common search patterns and the existing entity model. The product owner should confirm these are the correct filters; additional filters (e.g., license type for packages, SBOM source) may be needed.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` route handler to accept new query parameters: `entity_type` (optional enum: sbom|advisory|package), `severity` (optional string), `date_from` (optional ISO date), `date_to` (optional ISO date); pass these to the search service
- `modules/search/src/service/mod.rs` — Update `SearchService` search method to accept a filter struct and call `apply_filters` from `common/src/db/query.rs` to apply filter predicates before executing the query

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `entity_type` (enum: sbom|advisory|package), `severity` (string, filters advisories by severity level), `date_from` (ISO 8601 date, inclusive), `date_to` (ISO 8601 date, inclusive). All parameters are optional; omitting them returns unfiltered results (backward compatible).

## Implementation Notes
- Define a `SearchFilters` struct in the search module (or in the endpoint handler) with optional fields for each filter parameter. Use Axum's `Query<SearchFilters>` extractor to deserialize from query string.
- The `entity_type` filter restricts which entity tables are queried — if set to "sbom", only search the SBOM table. If not set, search all entity tables (current behavior).
- The `severity` filter applies only when searching advisories. Reference the `severity` field in `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).
- Date range filters apply to entity creation/modification timestamps.
- Use the `apply_filters` helper from `common/src/db/query.rs` (Task 2) to apply filter predicates to the query.
- Return results using `PaginatedResults<T>` from `common/src/model/paginated.rs` — this is the standard list response wrapper.
- Per Key Conventions §Response types: list/search endpoints must return `PaginatedResults<T>`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.
- Per Key Conventions §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust source file scope.
- Per Key Conventions §Endpoint registration: ensure route registration in `modules/search/src/endpoints/mod.rs` is updated if the handler signature changes. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `common/src/db/query.rs::apply_filters` — Filter application helper (from Task 2)
- `common/src/db/query.rs` — Existing pagination and sorting helpers to compose with filters
- `common/src/model/paginated.rs::PaginatedResults` — Standard paginated response wrapper
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for the `severity` field used in severity filtering
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for list endpoint pattern with query parameter extraction

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory&severity=critical` returns only critical advisories
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns results within date range
- [ ] `GET /api/v2/search` without filter parameters returns all results (backward compatible)
- [ ] Filters compose with full-text search query parameter (search + filter simultaneously)
- [ ] Filters compose with existing pagination parameters
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOMs
- [ ] Integration test: search with `entity_type=advisory` returns only advisories
- [ ] Integration test: search with `severity=critical` filters advisory results by severity
- [ ] Integration test: search with date range returns results within the specified range
- [ ] Integration test: search with multiple filters applied simultaneously
- [ ] Integration test: search with no filters returns all entity types (backward compatibility)
- [ ] Integration test: search with invalid entity_type returns 400 error

## Dependencies
- Depends on: Task 2 — Add full-text query helpers (apply_filters helper must be available)
- Depends on: Task 3 — Upgrade search service to full-text (search service must be updated before adding filter composition)
