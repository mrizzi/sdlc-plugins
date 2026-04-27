# Task 3 — Add search filter parameters to the search endpoint

**Feature:** TC-9002 — Improve search experience
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Description
Extend the `GET /api/v2/search` endpoint to accept filter query parameters, allowing users to narrow search results by entity type, severity (for advisories), and date range. This addresses the MVP requirement "Add filters — some kind of filtering capability."

**Ambiguity flag:** The feature specifies "some kind of filtering capability" without defining which filters. This task assumes the following filters based on the data model:
- `entity_type` — filter by entity kind: `sbom`, `advisory`, `package` (or combination)
- `severity` — filter advisories by severity level (requires the `severity` field on `AdvisorySummary`)
- `date_from` / `date_to` — filter by creation or modification date range

The product owner should confirm whether these filters are correct and whether additional filters are needed (e.g., license type for packages, specific SBOM fields).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters (`entity_type`, `severity`, `date_from`, `date_to`) to the search endpoint handler; parse and validate filter values
- `modules/search/src/service/mod.rs` — Extend `SearchService` to accept filter parameters and apply them as WHERE clauses in the search query

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchFilter` struct to hold parsed filter parameters (entity type enum, optional severity, optional date range)

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `entity_type` (string, comma-separated): filter by entity type (`sbom`, `advisory`, `package`)
  - `severity` (string): filter advisories by severity level
  - `date_from` (ISO 8601 date string): filter results created on or after this date
  - `date_to` (ISO 8601 date string): filter results created on or before this date

## Implementation Notes
- Inspect the existing search endpoint in `modules/search/src/endpoints/mod.rs` to understand the current query parameter handling pattern
- Reference the filtering patterns in `common/src/db/query.rs` — this module already contains shared query builder helpers for filtering and pagination. Reuse these helpers rather than implementing custom filter logic
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field — use this for severity filtering
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field — this could be a future filter candidate but is out of scope for this task
- Entity types correspond to the SeaORM entities in `entity/src/`: `sbom.rs`, `advisory.rs`, `package.rs`
- Filters should be combinable via AND logic (all specified filters must match)
- Invalid filter values should return a 400 Bad Request with a descriptive error message, following the `AppError` pattern in `common/src/error.rs`
- Per docs/constraints.md Section 5.4: reuse existing filtering utilities in `common/src/db/query.rs`
- Per docs/constraints.md Section 2 (Commit Rules): commit must reference TC-9002 in the footer

## Reuse Candidates
- `common/src/db/query.rs` — Shared filtering, pagination, and sorting query helpers; primary reuse target for filter construction
- `common/src/error.rs` — `AppError` enum for returning validation errors on invalid filter parameters
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field used for severity filter validation
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of a list endpoint with query parameters; follow the same pattern for filter parameter extraction

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Multiple filters combine via AND logic
- [ ] Invalid filter values return 400 Bad Request with a descriptive error
- [ ] Omitting all filters returns results as before (backward compatible)
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM entities
- [ ] Integration test: search with `entity_type=advisory` returns only advisory entities
- [ ] Integration test: search with `severity=high` returns only matching advisories
- [ ] Integration test: search with date range returns only results within the range
- [ ] Integration test: search with combined filters (entity_type + severity) returns correct intersection
- [ ] Integration test: search with invalid filter value returns 400 status
- [ ] Integration test: search without filters returns all entity types (backward compatibility)

## Verification Commands
- `cargo test -p tests --test search` — all search tests pass
- `cargo test -p modules-search` — module-level tests pass

## Dependencies
- Depends on: Task 1 — Add database indexes for search performance (indexes should cover filter columns for efficient filtered queries)
