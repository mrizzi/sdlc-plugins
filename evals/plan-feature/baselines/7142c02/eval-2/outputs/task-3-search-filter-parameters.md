## Repository
trustify-backend

## Target Branch
main

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": ["RHTPA 1.6.0"]}

## Description
Add filter parameters to the search endpoint so users can narrow search results by entity type, severity, and date range. The feature requires "some kind of filtering capability" but does not specify which filter dimensions to support.

**Assumption (pending clarification):** The feature description says "Add filters — Some kind of filtering capability" without specifying filter dimensions, operators, or interaction behavior. This task assumes the following filter parameters based on the entity model structure visible in the repository:
- `entity_type` — filter by result type (sbom, advisory, package)
- `severity` — filter advisories by severity level (uses the `severity` field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`)
- `date_from` / `date_to` — filter by creation or publication date range

These filter choices are assumptions pending product owner clarification. Additional filters (e.g., license type from `entity/src/package_license.rs`) may be needed.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter structs for filter extraction (`entity_type`, `severity`, `date_from`, `date_to`). Parse and validate filter values before passing to service layer.
- `modules/search/src/service/mod.rs` — Extend `SearchService` search method to accept filter parameters and apply them as `WHERE` clause conditions in addition to the full-text search query.
- `common/src/db/query.rs` — Add reusable filter builder functions for entity type enum matching, severity enum matching, and date range filtering. Follow the existing helper pattern for filtering and pagination.

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters: `entity_type` (string enum: `sbom`, `advisory`, `package`), `severity` (string enum matching advisory severity levels), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). All filters are optional and combine with AND semantics. Invalid filter values return `400 Bad Request`.

## Implementation Notes
- Extract filter parameters using Axum's `Query<FilterParams>` extractor in `modules/search/src/endpoints/mod.rs`, following the same pattern used for pagination parameters in sibling endpoints like `modules/fundamental/src/sbom/endpoints/list.rs`.
- In `modules/search/src/service/mod.rs`, apply filters as additional `WHERE` conditions using SeaORM's `Condition::all()` builder. Each filter is optional — only add the condition if the parameter is present.
- Reuse the existing query builder patterns in `common/src/db/query.rs` for constructing filter conditions. The existing helpers for filtering and pagination demonstrate the pattern for building `Condition` objects.
- The severity filter only applies when results include advisories — when `entity_type` is set to `sbom` or `package`, the severity filter should be ignored (not cause an error).
- Date range filters should use inclusive bounds: `date_from <= created_at AND created_at <= date_to`.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint scope.

## Reuse Candidates
- `common/src/db/query.rs` — existing filtering and pagination helpers. The new filter builders should follow the same patterns and be co-located here.
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of query parameter extraction with `Query<>` in a list endpoint. Follow this pattern for the search filter parameters.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field definition. Use the same severity enum for filter validation.

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?severity=high` returns only advisories with high severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Multiple filters combine with AND semantics (e.g., `entity_type=advisory&severity=high`)
- [ ] Invalid filter values return `400 Bad Request` with a descriptive error message
- [ ] Omitting all filters returns unfiltered results (backward-compatible)
- [ ] Filters work correctly in combination with the search query and relevance sorting from Task 2

## Test Requirements
- [ ] Integration test: `entity_type=sbom` returns only SBOM results
- [ ] Integration test: `entity_type=advisory` returns only advisory results
- [ ] Integration test: `severity=high` filters to high-severity advisories only
- [ ] Integration test: date range filter returns only results within the specified range
- [ ] Integration test: combining multiple filters narrows results correctly
- [ ] Integration test: invalid `entity_type` value returns 400 status
- [ ] Integration test: invalid date format returns 400 status
- [ ] Integration test: no filters returns all results (backward compatibility)

## Dependencies
- Depends on: Task 2 — Implement relevance-scored search ranking (filters should work in combination with the relevance scoring)

[sdlc-workflow] Description digest: sha256-md:e87701d4db67fb8c399143448cc825af6672f785ed751608a1b1283ce53c01e4
