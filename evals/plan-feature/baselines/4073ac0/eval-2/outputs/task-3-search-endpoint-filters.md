## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the search endpoint (`GET /api/v2/search`) so users
can narrow search results by entity type, severity, date range, and other fields.
This addresses the "Add filters — some kind of filtering capability" requirement
from TC-9002.

ASSUMPTION (pending clarification): Filters will include entity type (sbom, advisory,
package), severity (for advisories), date range (for SBOMs), and license (for packages).
Filters use AND semantics when combined.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to the `GET /api/v2/search` handler: `entity_type`, `severity`, `date_from`, `date_to`, `license`. Parse these from query string and pass to SearchService
- `modules/search/src/service/mod.rs` — Extend search method to accept a filter struct and apply filter predicates to the full-text search query

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `entity_type` (enum: sbom, advisory, package), `severity` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date), `license` (string). All filters are optional; when multiple are provided, they combine with AND semantics.

## Implementation Notes
The search endpoint is in `modules/search/src/endpoints/mod.rs` (`GET /api/v2/search`).
Add an Axum `Query<SearchFilters>` extractor struct with optional fields for each
filter parameter. Use `#[serde(default)]` for optional deserialization.

In `modules/search/src/service/mod.rs`, extend the search method signature to accept
filter parameters. Apply filters as additional WHERE clauses on the search query:
- `entity_type`: filter to only the specified entity table(s)
- `severity`: match against `AdvisorySummary.severity` field (see `modules/fundamental/src/advisory/model/summary.rs`)
- `date_from`/`date_to`: range filter on SBOM timestamp fields
- `license`: match against `PackageSummary.license` field (see `modules/fundamental/src/package/model/summary.rs`)

Use the shared query builder helpers in `common/src/db/query.rs` for constructing
filter predicates, following the existing filtering patterns.

Return `Result<T, AppError>` with `.context()` wrapping per the error handling
convention in `common/src/error.rs`.

Per CONVENTIONS.md §Query helpers: Shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Error handling: All handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Reuse existing filtering and pagination helpers rather than writing new filter predicate logic from scratch
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference the severity field definition for filter validation
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Reference the license field definition for filter validation

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only SBOMs within the date range
- [ ] `GET /api/v2/search?license=MIT` returns only packages with MIT license
- [ ] Multiple filters combine with AND semantics
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Omitting all filters returns unfiltered results (backward compatible)

## Test Requirements
- [ ] Filtering by entity_type returns only the specified entity type
- [ ] Filtering by severity returns matching advisories only
- [ ] Date range filtering returns SBOMs within the specified range
- [ ] License filtering returns matching packages only
- [ ] Combined filters narrow results correctly (AND semantics)
- [ ] Invalid filter values produce 400 responses with descriptive error messages
- [ ] No filters provided returns the same results as before (backward compatibility)

## Dependencies
- Depends on: Task 2 — Enhance SearchService with relevance-scored full-text search
