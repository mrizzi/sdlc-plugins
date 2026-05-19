## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint so users can narrow search results by entity type and entity-specific fields. This addresses the "Add filters" requirement from TC-9002.

**Assumption (pending clarification -- see A3 in impact map):** The feature description says "some kind of filtering capability" without specifying which filters. This task assumes the following filter set based on the entity model fields visible in the repository structure:
- `type` filter: narrow results to a specific entity type (sbom, advisory, package)
- `severity` filter: for advisories, filter by severity level (from `AdvisorySummary.severity`)
- `license` filter: for packages, filter by license (from `PackageSummary.license`)

These filter fields are assumptions. The exact set of filters should be confirmed with the product owner before implementation begins. Filter combination logic is assumed to be AND (all filters must match).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add filter query parameters (`type`, `severity`, `license`) to the search endpoint; parse and validate filter values
- `modules/search/src/service/mod.rs` -- Apply filter predicates to the search query; combine filters with AND logic alongside full-text search
- `common/src/db/query.rs` -- Add reusable filter predicate builder functions if not already generic enough for the new filter types
- `tests/api/search.rs` -- Add integration tests for all filter combinations

## API Changes
- `GET /api/v2/search` -- MODIFY: Add optional query parameters: `type` (values: `sbom`, `advisory`, `package`), `severity` (values: `low`, `medium`, `high`, `critical`), `license` (free-text match). All filters are optional. When multiple filters are provided, they combine with AND logic. Invalid filter values return 400 Bad Request with a descriptive error message.

## Implementation Notes
- Follow the filtering pattern already established in `common/src/db/query.rs` -- the shared query builder helpers already support filtering and pagination. Extend these patterns rather than creating a separate filter mechanism.
- In `modules/search/src/endpoints/mod.rs`:
  - Add a `SearchFilters` struct with optional fields for each filter parameter
  - Deserialize from query string using the same pattern as other list endpoints (see `modules/fundamental/src/advisory/endpoints/list.rs` for how query parameters are structured)
  - Validate enum values for `type` and `severity`; return `AppError` for invalid values
- In `modules/search/src/service/mod.rs`:
  - When `type` filter is provided, restrict the search to that entity type only (skip queries against other entity tables)
  - When `severity` filter is provided, add a WHERE clause on the advisory severity field; if `type` is not `advisory`, the `severity` filter is ignored (or returns empty results for non-advisory types)
  - When `license` filter is provided, add a WHERE clause matching the package license field; similar type-scoping logic applies
  - Combine filters with AND logic: `WHERE search_vector @@ query AND severity = $1 AND ...`
- Use `common/src/error.rs::AppError` for validation errors (invalid filter values), following the existing error handling pattern with `.context()` wrapping
- The `severity` enum values should match whatever values are stored in the advisory entity's severity field (examine `entity/src/advisory.rs` and `modules/fundamental/src/advisory/model/summary.rs` for the field type)
- The `license` filter should use case-insensitive partial matching (ILIKE) since license strings may vary in format

## Reuse Candidates
- `common/src/db/query.rs` -- Existing filter and pagination helpers; extend for new filter types
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Query parameter parsing pattern to follow
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Severity field definition; use the same type/enum for the severity filter
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- License field definition; understand the field type for the license filter
- `common/src/error.rs::AppError` -- Validation error handling

## Acceptance Criteria
- [ ] Search endpoint accepts optional `type` filter parameter with values `sbom`, `advisory`, `package`
- [ ] Search endpoint accepts optional `severity` filter parameter for advisory results
- [ ] Search endpoint accepts optional `license` filter parameter for package results
- [ ] Filters combine with AND logic when multiple are provided
- [ ] Invalid filter values return 400 Bad Request with a descriptive error message
- [ ] Filters work correctly in combination with the `q` search parameter and `sort` parameter from Task 2
- [ ] When no filters are provided, behavior is unchanged from Task 2 (backward compatible)
- [ ] Entity-specific filters (severity, license) are scoped correctly: severity only applies to advisories, license only applies to packages

## Test Requirements
- [ ] Integration test: search with `type=advisory`, verify only advisory results returned
- [ ] Integration test: search with `type=sbom`, verify only SBOM results returned
- [ ] Integration test: search with `severity=high`, verify only high-severity advisories returned
- [ ] Integration test: search with `license=MIT` (or similar), verify only matching packages returned
- [ ] Integration test: search with `type=advisory&severity=critical`, verify combined filter
- [ ] Integration test: search with `severity=invalid_value`, verify 400 response
- [ ] Integration test: search with filters and `q` parameter combined, verify both filtering and full-text search work together
- [ ] Integration test: search with no filters, verify unchanged behavior

## Verification Commands
- `cargo test --test api` -- all integration tests pass including new filter tests

## Dependencies
- Depends on: Task 2 -- Implement relevance-ranked search using full-text search
