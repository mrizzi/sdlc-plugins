# Task 3 — Add filtering parameters to search endpoint

**Summary:** Extend GET /api/v2/search with entity type, date range, and severity filters

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search endpoint (`GET /api/v2/search`) to accept optional query parameters for filtering results by entity type (sbom, advisory, package), date range (created/modified after/before), and advisory severity. This addresses the "Add filters — some kind of filtering capability" MVP requirement. The filters narrow results before full-text ranking is applied, improving both relevance and performance for users who know what category of results they need.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add filter parameters to the search method signature and apply them as WHERE clauses in the full-text search query
- `modules/search/src/endpoints/mod.rs` — Parse new query parameters (`entity_type`, `created_after`, `created_before`, `severity`) from the request and pass them to `SearchService`

## Files to Create
- `modules/search/src/model/mod.rs` — Define a `SearchFilters` struct to encapsulate filter parameters (entity_type: Option<EntityType>, created_after: Option<DateTime>, created_before: Option<DateTime>, severity: Option<String>) and a `SearchQuery` struct combining the search term with filters

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, optional) — Filter by entity type: `sbom`, `advisory`, or `package`
  - `created_after` (ISO 8601 datetime, optional) — Only return results created after this timestamp
  - `created_before` (ISO 8601 datetime, optional) — Only return results created before this timestamp
  - `severity` (string, optional) — Filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`)
  - All parameters are optional; omitting them returns unfiltered results (backward compatible)

## Implementation Notes
- Use the shared query builder helpers in `common/src/db/query.rs` for building filter conditions — examine how existing list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`, `modules/fundamental/src/advisory/endpoints/list.rs`) parse and apply query parameters for pagination and filtering.
- The `entity_type` filter should control which tables are queried in the full-text search — when set, only search the specified entity table rather than all three.
- Date range filters should apply to the entity's creation timestamp column.
- The `severity` filter only applies to advisory entities — if `entity_type` is set to `sbom` or `package`, the severity filter should be ignored (or return an error, depending on team preference).
- Follow the Axum query parameter extraction pattern used in other endpoints (likely `Query<T>` extractor).
- Use the `AdvisorySummary` struct's severity field (see `modules/fundamental/src/advisory/model/summary.rs`) to understand the severity data model.
- Ensure the filter struct derives `Deserialize` for automatic Axum query parameter parsing.

## Reuse Candidates
- `common/src/db/query.rs` — Shared filtering helpers; extend with search-specific filter logic rather than building from scratch.
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for how list endpoints parse query parameters with Axum's `Query<T>` extractor.
- `modules/fundamental/src/advisory/endpoints/list.rs` — Reference for advisory-specific filtering patterns.
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct contains the severity field definition.
- `modules/fundamental/src/sbom/model/summary.rs` — `SbomSummary` struct for SBOM result shape.
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct; contains the license field for potential future filtering.

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?q=term&created_after=2024-01-01T00:00:00Z` returns only results created after the given date
- [ ] `GET /api/v2/search?q=term&severity=critical` returns only critical-severity advisories
- [ ] All filter parameters are optional — omitting them returns all results (backward compatible)
- [ ] Filter parameters can be combined (e.g., `entity_type=advisory&severity=high`)
- [ ] Invalid filter values return appropriate error responses via `AppError`

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `entity_type=advisory` returns only advisory results
- [ ] Integration test: search with `entity_type=package` returns only package results
- [ ] Integration test: search with date range filters returns only results within the range
- [ ] Integration test: search with `severity=critical` returns only matching advisories
- [ ] Integration test: search with combined filters (entity_type + severity) works correctly
- [ ] Integration test: search with no filters returns all entity types (backward compatibility)

## Verification Commands
- `cargo test --test search` — All search integration tests pass

## Dependencies
- Depends on: Task 2 — Optimize SearchService with PostgreSQL full-text search
