## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the entity list endpoints (`GET /api/v2/sbom`,
`GET /api/v2/advisory`, `GET /api/v2/package`) so users can filter results by
entity-specific fields. This extends the filtering capability from Task 3 to the
individual entity list endpoints, providing a consistent filtering experience
across the API.

ASSUMPTION (pending clarification): Each entity list endpoint gets filters relevant
to its domain: SBOMs by date range and name, advisories by severity, and packages
by license and name.

## Files to Modify
- `common/src/db/query.rs` — Add shared filter predicate builder functions (date range, severity enum, license string match) that can be reused across all entity list endpoints
- `modules/fundamental/src/sbom/endpoints/list.rs` — Add `name`, `date_from`, `date_to` filter query parameters to `GET /api/v2/sbom`
- `modules/fundamental/src/advisory/endpoints/list.rs` — Add `severity`, `title` filter query parameters to `GET /api/v2/advisory`
- `modules/fundamental/src/package/endpoints/list.rs` — Add `license`, `name` filter query parameters to `GET /api/v2/package`

## API Changes
- `GET /api/v2/sbom` — MODIFY: Add optional query parameters `name` (string, partial match), `date_from` (ISO 8601), `date_to` (ISO 8601)
- `GET /api/v2/advisory` — MODIFY: Add optional query parameters `severity` (string), `title` (string, partial match)
- `GET /api/v2/package` — MODIFY: Add optional query parameters `license` (string), `name` (string, partial match)

## Implementation Notes
Each list endpoint already returns `PaginatedResults<T>` from
`common/src/model/paginated.rs`. The filter parameters should be added as an Axum
`Query<T>` extractor struct alongside the existing pagination parameters.

In `common/src/db/query.rs`, add reusable filter helper functions:
- `apply_date_range_filter(query, column, from, to)` — adds WHERE clauses for date range
- `apply_string_filter(query, column, value)` — adds WHERE ILIKE clause for partial string match
- `apply_exact_filter(query, column, value)` — adds WHERE = clause for exact match

These helpers follow the existing pattern in `common/src/db/query.rs` (shared query
builder helpers for filtering, pagination, sorting) and should be designed for reuse
across all entity endpoints.

Each endpoint handler should validate filter parameters and return `AppError` for
invalid values, following the error handling pattern in `common/src/error.rs`.

The list endpoint handlers reference their respective services:
- `modules/fundamental/src/sbom/service/sbom.rs` — SbomService (may need filter parameter passthrough)
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService (may need filter parameter passthrough)
- `modules/fundamental/src/package/service/mod.rs` — PackageService (may need filter parameter passthrough)

Per CONVENTIONS.md §Query helpers: Shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `common/src/db/query.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response types: List endpoints return `PaginatedResults<T>`.
Applies: task modifies `modules/fundamental/src/sbom/endpoints/list.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: All handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Extend existing shared filtering infrastructure rather than implementing filter logic inline in each endpoint
- `common/src/model/paginated.rs::PaginatedResults<T>` — Existing response wrapper; no changes needed but filters must preserve pagination behavior
- `common/src/error.rs::AppError` — Use for filter validation error responses

## Acceptance Criteria
- [ ] `GET /api/v2/sbom?name=linux` returns only SBOMs with "linux" in the name
- [ ] `GET /api/v2/sbom?date_from=2024-01-01&date_to=2024-06-30` returns SBOMs within the date range
- [ ] `GET /api/v2/advisory?severity=critical` returns only critical advisories
- [ ] `GET /api/v2/advisory?title=CVE` returns advisories with "CVE" in the title
- [ ] `GET /api/v2/package?license=MIT` returns only MIT-licensed packages
- [ ] `GET /api/v2/package?name=openssl` returns only packages with "openssl" in the name
- [ ] Pagination continues to work correctly with filters applied
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return 400 Bad Request with descriptive error messages

## Test Requirements
- [ ] Each filter parameter on each endpoint returns correctly filtered results
- [ ] Date range filters handle edge cases (from only, to only, from > to)
- [ ] String filters perform case-insensitive partial matching
- [ ] Filters combined with pagination produce correct page counts and results
- [ ] No filters returns the same results as before (backward compatibility)
- [ ] Invalid filter values produce 400 responses

## Dependencies
- Depends on: Task 2 — Enhance SearchService with relevance-scored full-text search (for shared query infrastructure patterns)
