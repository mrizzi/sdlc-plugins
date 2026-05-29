## Repository
trustify-backend

## Target Branch
main

## Description
Add filter support to the search endpoint, allowing users to narrow search results by entity type, severity (for advisories), and date range. This addresses the TC-9002 requirement for "some kind of filtering capability."

**Ambiguity note:** The feature description (TC-9002) specifies "Add filters — Some kind of filtering capability" but does not define which fields to filter on, what filter types are needed, whether filters are combinable, or what the filter UX should be. This task assumes the following filter set based on the existing entity model:
- **Entity type filter:** SBOM, Advisory, Package (enum-based, multi-select)
- **Severity filter:** for Advisory results, based on the `severity` field in `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`)
- **Date range filter:** created/modified date range for all entity types

The product owner should confirm this filter set and specify whether filters use AND-combination (default assumption) or support OR logic.

## Files to Modify
- `modules/search/src/service/mod.rs` — Extend `SearchService` methods to accept and apply filter parameters
- `modules/search/src/endpoints/mod.rs` — Add query parameter parsing for filter fields (entity_type, severity, date_from, date_to)
- `common/src/db/query.rs` — Add shared filter builder helpers for entity type, severity, and date range filtering if not already present

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchFilter` struct to represent filter parameters (entity_type, severity, date_from, date_to)

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters: `entity_type` (comma-separated list: sbom,advisory,package), `severity` (e.g., critical,high,medium,low), `date_from` (ISO 8601), `date_to` (ISO 8601). All filters are optional; when omitted, no filtering is applied (current behavior preserved).

## Implementation Notes
- Define a `SearchFilter` struct in a new `modules/search/src/model/mod.rs` file following the module pattern used by other modules (e.g., `modules/fundamental/src/sbom/model/mod.rs`).
- Parse filter query parameters in the endpoint handler at `modules/search/src/endpoints/mod.rs` using Axum's `Query` extractor, consistent with the query parameter handling pattern in `modules/fundamental/src/sbom/endpoints/list.rs`.
- Apply filters as SQL `WHERE` clauses in the `SearchService`, composing them with the full-text search query. Use AND-combination for multiple filters.
- Leverage the existing query builder helpers in `common/src/db/query.rs` for filter construction. The module already provides shared filtering and pagination patterns — extend it with reusable filter helpers for entity type, severity enum matching, and date range comparisons.
- The `severity` field is available on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` — use this as reference for the severity enum values.
- The `license` field is available on `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` — note this for potential future filter extension.
- Follow error handling with `Result<T, AppError>` from `common/src/error.rs` for invalid filter values (e.g., invalid date format, unknown entity type).

**Assumption (pending clarification):** Filter combination logic is assumed to be AND (all filters must match). The product owner should confirm whether OR logic between filter groups is needed.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Existing filtering and pagination utilities to extend with new filter types rather than creating parallel filter logic
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Contains the `severity` field definition; reuse the severity enum/type for filter validation
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of query parameter parsing with Axum `Query` extractor; follow this pattern for filter parameter extraction

## Acceptance Criteria
- [ ] The search endpoint accepts optional filter query parameters: `entity_type`, `severity`, `date_from`, `date_to`
- [ ] Filtering by entity type correctly restricts results to only the specified entity types
- [ ] Filtering by severity correctly restricts advisory results to matching severity levels
- [ ] Date range filtering correctly restricts results to entities within the specified range
- [ ] Multiple filters can be combined (AND logic) in a single request
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Invalid filter values return appropriate error responses (not 500 errors)
- [ ] Results continue to be returned as `PaginatedResults<T>` with pagination support

## Test Requirements
- [ ] Integration test filtering by single entity type (e.g., only SBOMs)
- [ ] Integration test filtering by multiple entity types (e.g., SBOMs and Advisories)
- [ ] Integration test filtering by severity for advisory results
- [ ] Integration test filtering by date range
- [ ] Integration test combining multiple filters (entity type + severity + date range)
- [ ] Integration test verifying that omitting filters returns all results
- [ ] Integration test verifying error response for invalid filter values (bad date format, unknown entity type)

## Dependencies
- Depends on: Task 2 — Refactor SearchService for full-text search with relevance ranking

[sdlc-workflow] Description digest: sha256:0fa18640e0e619cba1c735d1187eb413c1af7b5668a957ced86a76b5d2816201
