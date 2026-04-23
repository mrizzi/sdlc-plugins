## Repository
trustify-backend

## Description
Add filtering capability to the search endpoint so users can narrow search results by entity type, severity, and date range. Filters are applied as additional WHERE clauses on the search query and are combined with AND logic. This addresses the MVP requirement "Add filters -- Some kind of filtering capability."

**ASSUMPTION -- pending clarification**: The specific filters to implement are assumed to be: `entity_type` (enum: sbom, advisory, package), `severity` (for advisories, e.g., critical, high, medium, low), and date range (`created_after`, `created_before` as ISO 8601 timestamps). The feature requirements say "some kind of filtering" without specifying which fields. This assumption needs validation with the product owner.

**ASSUMPTION -- pending clarification**: Filters are AND-combined (all conditions must match). The requirements do not specify whether OR logic should be supported. AND-only is assumed for MVP simplicity.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add query parameter parsing for filter fields (`entity_type`, `severity`, `created_after`, `created_before`). Pass parsed filters to the `SearchService`.
- `modules/search/src/service/mod.rs` -- Accept filter parameters in the search method and apply them as additional query conditions. Use the shared query builder from `common/src/db/query.rs` for consistent filter application.

## Files to Create
- `modules/search/src/model/mod.rs` -- Define a `SearchFilter` struct to represent the filter parameters and a `SearchEntityType` enum for the entity type filter. This follows the module pattern used by other modules (e.g., `modules/fundamental/src/sbom/model/mod.rs`).

## API Changes
- `GET /api/v2/search` -- MODIFY: Add optional query parameters: `entity_type` (string enum: sbom, advisory, package), `severity` (string enum: critical, high, medium, low -- only applies when entity_type=advisory), `created_after` (ISO 8601 datetime), `created_before` (ISO 8601 datetime).

## Implementation Notes
- Follow the filtering pattern established in `common/src/db/query.rs`, which provides shared query builder helpers for filtering, pagination, and sorting. The search filter logic should reuse these helpers rather than implementing custom filtering.
- The `SearchFilter` struct should be deserializable from query parameters using serde/axum extractors, consistent with how other endpoints in the codebase parse query parameters (see `modules/fundamental/src/sbom/endpoints/list.rs` for the list endpoint pattern).
- When `entity_type` is specified, only search the corresponding table(s). When not specified, search all entity types (current behavior).
- The `severity` filter should reference the severity field on `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs`). If `severity` is provided without `entity_type=advisory`, return a 400 error explaining that severity filtering requires entity_type=advisory.
- Date range filters apply to the creation timestamp of each entity.
- Error handling: invalid filter values should return `400 Bad Request` via the `AppError` enum in `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder helpers for filtering and pagination. Extend or reuse for search-specific filters.
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Example of a list endpoint with query parameter parsing for filtering and pagination. Follow this pattern for the filter parameter deserialization.
- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct includes the severity field. Reference this for severity filter values.
- `common/src/error.rs` -- `AppError` enum for returning structured 400 errors on invalid filter input.

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical&entity_type=advisory` returns only critical-severity advisories
- [ ] `GET /api/v2/search?severity=high` without entity_type returns 400 error
- [ ] `GET /api/v2/search?created_after=2024-01-01T00:00:00Z` returns only results created after the specified date
- [ ] `GET /api/v2/search?created_before=2024-06-01T00:00:00Z` returns only results created before the specified date
- [ ] Multiple filters can be combined: `entity_type=advisory&severity=high&created_after=2024-01-01T00:00:00Z`
- [ ] Invalid filter values return 400 Bad Request with a descriptive error message
- [ ] Filters work correctly in combination with the full-text search query parameter

## Test Requirements
- [ ] Integration test: search with `entity_type=advisory` returns only advisories
- [ ] Integration test: search with `entity_type=sbom` returns only SBOMs
- [ ] Integration test: search with `severity=critical&entity_type=advisory` returns filtered results
- [ ] Integration test: search with `severity=high` (no entity_type) returns 400 error
- [ ] Integration test: search with `created_after` and `created_before` returns date-filtered results
- [ ] Integration test: combined filters (entity_type + severity + date range + search query) return correctly filtered and ranked results
- [ ] Integration test: invalid enum value for entity_type returns 400 error

## Dependencies
- Depends on: Task 2 -- Optimize SearchService for performance and relevance ranking
