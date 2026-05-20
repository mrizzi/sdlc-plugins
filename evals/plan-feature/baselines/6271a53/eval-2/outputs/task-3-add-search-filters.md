# Task 3 — Add filter parameters to the search endpoint

**Feature:** TC-9002 — Improve search experience
**Label:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Users need the ability to narrow down search results using filters. This task adds filtering capabilities to the search endpoint, allowing users to filter by entity type (SBOM, advisory, package), severity level (for advisories), date range, and license (for packages). This addresses the "Add filters" requirement and makes search results more actionable.

## Files to Modify
- `modules/search/src/service/mod.rs` — Extend `SearchService` to accept filter parameters and apply them as WHERE clause conditions when building search queries
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` endpoint to parse filter query parameters and pass them to the service layer
- `common/src/db/query.rs` — Extend the shared query builder with filter combinators for entity type, severity, date range, and license fields

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type=sbom|advisory|package` — filter results to a specific entity type
  - `severity=low|medium|high|critical` — filter advisory results by severity level
  - `date_from=YYYY-MM-DD` — filter results created/updated on or after this date
  - `date_to=YYYY-MM-DD` — filter results created/updated on or before this date
  - `license=<license-id>` — filter package results by license

## Implementation Notes
- **Query builder pattern:** The shared filtering helpers in `common/src/db/query.rs` already support filtering and pagination. Extend these with new filter predicates for the search-specific parameters. Follow the existing pattern for how filters are applied to queries.
- **Entity-specific filters:** Some filters (severity, license) only apply to specific entity types. When `entity_type` is not specified but a type-specific filter is provided (e.g., `severity=high`), implicitly restrict results to the applicable entity type (advisories for severity, packages for license). Document this behavior in the endpoint.
- **Model references:** The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field. The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a license field. Use these existing fields for filter matching.
- **Entity definitions:** Review `entity/src/advisory.rs` for severity column definition and `entity/src/package_license.rs` for license mapping to ensure filters target the correct database columns.
- **Error handling:** Return `AppError` with appropriate HTTP 400 status for invalid filter values (e.g., unknown severity level, malformed date). Follow the error handling pattern in `common/src/error.rs`.
- **Constraint §5.2:** Read the current search endpoint and service implementation before adding filter logic.
- **Constraint §5.4:** Reuse existing query builder filtering patterns from `common/src/db/query.rs` rather than writing custom WHERE clause logic.
- **Constraint §5.8:** Compare with list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` which already support some form of filtering — ensure parity on error handling and parameter validation patterns.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Existing filtering infrastructure to extend with search-specific filters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains severity field used for filter matching
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — Contains license field used for filter matching
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of a list endpoint with filtering, pagination, and sorting to follow as a pattern
- `common/src/error.rs::AppError` — Error enum for returning validation errors on invalid filter parameters

## Acceptance Criteria
- [ ] The search endpoint accepts `entity_type`, `severity`, `date_from`, `date_to`, and `license` query parameters
- [ ] Providing `entity_type=sbom` returns only SBOM results
- [ ] Providing `severity=critical` returns only advisories with critical severity
- [ ] Date range filters correctly narrow results by creation/update date
- [ ] License filter returns only packages matching the specified license
- [ ] Invalid filter values return HTTP 400 with a descriptive error message
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Filters compose correctly with the search query (e.g., `q=openssl&severity=high` returns high-severity advisories matching "openssl")

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying entity_type filter returns only the specified entity type
- [ ] Integration test verifying severity filter returns only advisories with matching severity
- [ ] Integration test verifying date range filter correctly narrows results
- [ ] Integration test verifying license filter returns only packages with the specified license
- [ ] Integration test verifying invalid filter values return HTTP 400
- [ ] Integration test verifying filter composition with search query works correctly
- [ ] Integration test verifying no filters returns the same results as before (backward compatibility)

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Optimize search query performance (relies on the full-text search infrastructure)
