# Task 4: Add Filter Parameters to Search Endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint `GET /api/v2/search` so users can narrow search results by entity type, severity, and other relevant fields. This addresses the TC-9002 requirement to "add filters" with "some kind of filtering capability."

**Assumption (pending clarification)**: The feature description specifies no filter types. This task assumes the following filters based on the entity model and common search UX patterns:
1. `entity_type` (string, optional) — filter by "sbom", "advisory", or "package" to scope results to a single entity type.
2. `severity` (string, optional) — filter advisory results by severity level (critical, high, medium, low). Only applicable when `entity_type=advisory` or when unscoped.
3. `license` (string, optional) — filter package results by license identifier. Only applicable when `entity_type=package` or when unscoped.
These filter choices should be validated with the product owner.

**Assumption (pending clarification)**: Filters are assumed to use AND semantics (all specified filters must match). The feature description does not specify whether filters should be combinable with OR logic. If OR semantics are needed, the query builder in `common/src/db/query.rs` would need additional combinators.

**Assumption (pending clarification)**: Filter values are assumed to be exact-match (e.g., `severity=critical` matches only critical). Range filters (e.g., "severity >= high") or date-range filters are not included in this task due to lack of specification, but could be added as a follow-up.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameters for `entity_type`, `severity`, and `license` to the `GET /api/v2/search` handler; pass filter values to `SearchService`
- `modules/search/src/service/mod.rs` — Accept filter parameters and apply them as `WHERE` conditions to search queries; use the shared filter helpers from `common/src/db/query.rs`
- `common/src/db/query.rs` — Add filter predicate builder functions for entity_type discrimination, severity matching, and license matching; follow the existing pattern of shared filtering helpers in this file

## Files to Create
- `modules/search/src/model/filters.rs` — Define a `SearchFilters` struct with optional fields: `entity_type: Option<String>`, `severity: Option<String>`, `license: Option<String>`; implement `TryFrom<Query>` or Axum extractor for query parameter parsing

## Implementation Notes
- Define a `SearchFilters` struct in `modules/search/src/model/filters.rs` with Axum's `#[derive(Deserialize)]` for automatic query parameter extraction. The struct should use `Option<String>` for all fields so filters are optional.
- In `modules/search/src/endpoints/mod.rs`, add `Query<SearchFilters>` as a parameter to the search handler, following the Axum pattern used by list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs`.
- In `modules/search/src/service/mod.rs`, apply filters as additional `WHERE` conditions:
  - `entity_type`: Controls which entity tables are queried. If `entity_type=sbom`, skip advisory and package queries entirely. If unset, query all three.
  - `severity`: Add `WHERE severity = ?` condition to the advisory query. The severity field exists on the advisory entity (`entity/src/advisory.rs`) and is surfaced in `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`).
  - `license`: Add a `JOIN` on `package_license` (`entity/src/package_license.rs`) with `WHERE license = ?` condition to the package query.
- Add reusable filter predicate functions in `common/src/db/query.rs` following the existing filtering helper pattern. These should accept a column reference and a value, returning a SeaORM `Condition`.
- Validate filter values at the endpoint layer: return `400 Bad Request` (via `AppError` from `common/src/error.rs`) for invalid severity values or unrecognized entity types.
- Update the `modules/search/src/model/mod.rs` (created in Task 3) to re-export the new `filters` submodule.

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?q=term&severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?q=term&license=MIT` returns only packages with MIT license
- [ ] Multiple filters can be combined: `?q=term&entity_type=package&license=Apache-2.0`
- [ ] Invalid filter values return `400 Bad Request` with a descriptive error message
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Filters work correctly with pagination (`PaginatedResults<SearchResult>`)
- [ ] Filter parameters are documented in the endpoint handler's doc comments

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `severity=critical` returns only critical-severity advisory results
- [ ] Integration test: search with `license=MIT` returns only packages with MIT license
- [ ] Integration test: search with no filters returns results from all entity types (backward compatibility)
- [ ] Integration test: search with invalid `entity_type` returns 400 status
- [ ] Integration test: combined filters (`entity_type=advisory&severity=high`) work correctly

## Dependencies
- Depends on: Task 3 — Improve Search Result Relevance Scoring (depends on the `SearchResult` response type)
