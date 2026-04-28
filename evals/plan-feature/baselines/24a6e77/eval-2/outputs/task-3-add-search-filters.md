# Task 3 — Add Filtering Parameters to Search Endpoint

## Repository
trustify-backend

## Description
Add filtering capabilities to the search endpoint (`GET /api/v2/search`) so users can narrow search results by entity type, date range, and domain-specific attributes (severity for advisories, license for packages). The feature requirement states "Add filters — some kind of filtering capability" as an MVP requirement. The filters are derived from existing entity fields: `AdvisorySummary` includes a `severity` field and `PackageSummary` includes a `license` field, making these natural filter dimensions.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add query parameter structs for filter extraction; update the `GET /api/v2/search` handler to pass filters to SearchService
- `modules/search/src/service/mod.rs` — extend search method signature to accept filter parameters and apply them as WHERE clause conditions alongside the full-text search query
- `common/src/db/query.rs` — add shared helper functions for date range filtering and enum-based filtering that can be reused by other modules

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters:
  - `entity_type` (string, optional): filter by entity type (`sbom`, `advisory`, `package`)
  - `date_from` (ISO 8601 date, optional): filter results created/updated on or after this date
  - `date_to` (ISO 8601 date, optional): filter results created/updated on or before this date
  - `severity` (string, optional): filter advisory results by severity level
  - `license` (string, optional): filter package results by license type

## Implementation Notes
- Inspect the current endpoint handler in `modules/search/src/endpoints/mod.rs` to understand the existing query parameter extraction pattern
- Use Axum's `Query<T>` extractor with a new `SearchFilters` struct for query parameter deserialization — follow the pattern used by list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs`
- The `entity_type` filter should control which entity tables are included in the search query (e.g., if `entity_type=advisory`, only search the advisory table)
- Date range filters should use `>=` and `<=` comparisons on the entity's created/updated timestamp columns
- `severity` filter applies only when searching advisories — see `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` for the severity field definition
- `license` filter applies only when searching packages — see `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` for the license field definition
- Add the new shared filter helpers to `common/src/db/query.rs` following the existing helper patterns in that file (filtering, pagination, sorting)
- Per constraints doc section 2: commit must reference TC-9002 in footer
- Per constraints doc section 5: keep changes scoped to listed files

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers for filtering, pagination, and sorting; extend with new filter helpers rather than duplicating
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of query parameter extraction pattern in list endpoints
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field definition for advisory filtering
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — license field definition for package filtering

## Acceptance Criteria
- [ ] Search endpoint accepts optional `entity_type` query parameter to filter by entity type
- [ ] Search endpoint accepts optional `date_from` and `date_to` query parameters for date range filtering
- [ ] Search endpoint accepts optional `severity` parameter for advisory filtering
- [ ] Search endpoint accepts optional `license` parameter for package filtering
- [ ] Filters compose correctly (e.g., `entity_type=advisory&severity=high` returns only high-severity advisories matching the search term)
- [ ] Omitting all filters preserves existing behavior (search across all entities)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request with descriptive message)

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `entity_type=advisory&severity=high` returns only high-severity advisory results
- [ ] Integration test: search with date range returns only results within the range
- [ ] Integration test: search with multiple filters applied simultaneously returns correct intersection
- [ ] Integration test: search with no filters returns results across all entity types (backward compatibility)
- [ ] Integration test: search with invalid `entity_type` value returns 400 error

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 2 — Refactor SearchService for Weighted Full-Text Search Ranking
