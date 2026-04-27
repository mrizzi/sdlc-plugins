## Repository
trustify-backend

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow search results by entity type (SBOM, advisory, package) and by advisory severity. This addresses the MVP requirement "Add filters" by introducing query parameters for entity-type and severity filtering.

**Ambiguity note:** The feature requirement specifies only "Some kind of filtering capability" with no details on which fields, which entities, or what filter types. This task assumes the following filters (assumption pending clarification with product owner):
- Entity type filter: allow searching only SBOMs, only advisories, only packages, or any combination
- Severity filter: for advisory results, allow filtering by severity level (e.g., critical, high, medium, low)

Additional filters (e.g., date range, license type, package namespace) may be added in follow-up tasks once the product owner clarifies filter requirements.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add new query parameters (`entity_type`, `severity`) to the search endpoint handler and pass them to the service layer
- `modules/search/src/service/mod.rs` — accept filter parameters and apply them as `WHERE` clause conditions in the search query

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional, repeatable): filter results by entity type. Accepted values: `sbom`, `advisory`, `package`. Multiple values can be specified (e.g., `?entity_type=sbom&entity_type=advisory`). Omitting this parameter returns all entity types (backward-compatible).
  - `severity` (string, optional, repeatable): filter advisory results by severity. Accepted values: `critical`, `high`, `medium`, `low`. Only applies to advisory entities; ignored for other entity types. Omitting returns all severities.

## Implementation Notes
- The existing search endpoint is defined in `modules/search/src/endpoints/mod.rs` and calls `SearchService` in `modules/search/src/service/mod.rs`.
- Add a new query parameter struct (or extend the existing one) to capture `entity_type` and `severity` parameters. Use Axum's `Query<T>` extractor.
- In `SearchService`, apply the filters as additional `WHERE` conditions:
  - Entity type filter: conditionally join/query only the specified entity tables. If the current search implementation unions results across SBOM, advisory, and package tables, add conditional logic to include only the requested entity types.
  - Severity filter: add a `WHERE advisory.severity IN (...)` clause when severity filter is present. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field — use the same enum/type for filter values.
- Leverage the existing query builder helpers in `common/src/db/query.rs` for filtering patterns. The codebase already has shared filtering and pagination utilities that should be extended or reused.
- Per Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. Invalid filter values (e.g., `entity_type=invalid`) should return a 400 Bad Request via `AppError`.
- Per Key Conventions: response type remains `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Validate filter values at the endpoint layer before passing to the service. Use Rust enums for type-safe filter values.

## Reuse Candidates
- `common/src/db/query.rs` — existing shared query builder helpers for filtering and pagination. Extend or follow these patterns for the new filter conditions.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field definition; use the same type for the severity filter enum.
- `common/src/model/paginated.rs::PaginatedResults<T>` — continue using for paginated response.
- `common/src/error.rs::AppError` — use for returning 400 errors on invalid filter values.

## Acceptance Criteria
- [ ] The `GET /api/v2/search` endpoint accepts an optional `entity_type` query parameter
- [ ] The `GET /api/v2/search` endpoint accepts an optional `severity` query parameter
- [ ] When `entity_type=sbom` is specified, only SBOM results are returned
- [ ] When `entity_type=advisory&severity=critical` is specified, only critical-severity advisory results are returned
- [ ] When no filters are specified, all entity types and severities are returned (backward-compatible)
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message
- [ ] Filters combine correctly with the full-text search query (from Task 2)
- [ ] Response format remains `PaginatedResults<T>` with correct pagination metadata

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: search with `entity_type=sbom` returns only SBOMs
- [ ] Integration test: search with `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Integration test: search with multiple entity types returns results from all specified types
- [ ] Integration test: search with no filters returns results from all entity types (backward compatibility)
- [ ] Integration test: search with invalid `entity_type` value returns 400 Bad Request
- [ ] Integration test: severity filter is ignored for non-advisory entity types (no error, just no effect)
- [ ] Integration test: filters work correctly in combination with a search query term

## Dependencies
- Depends on: Task 2 — Enhance search relevance ranking (filters build on the enhanced search query infrastructure)
