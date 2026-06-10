# Task 3 — Add filtering parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint so users can narrow search results by entity type, severity (for advisories), and license (for packages). The feature description says "add filters — some kind of filtering capability" but does not specify which fields should be filterable, what filter types to support, or which entities the filters apply to (**assumption pending clarification**: we will add filters for entity type, advisory severity, and package license, as these are the most useful fields based on the existing data model). This task addresses the "Add filters" MVP requirement from TC-9002.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter parameters in search queries
- `modules/search/src/endpoints/mod.rs` — update `GET /api/v2/search` endpoint to accept filter query parameters (`type`, `severity`, `license`)
- `common/src/db/query.rs` — extend query builder helpers to support the new filter predicates if not already covered by existing filtering helpers

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters: `type` (enum: `sbom`, `advisory`, `package`), `severity` (string, applies to advisories), `license` (string, applies to packages). Multiple values supported via comma separation (e.g., `type=sbom,advisory`). Filters are combined with AND semantics.

## Implementation Notes
- The existing query builder in `common/src/db/query.rs` already provides shared filtering, pagination, and sorting helpers. Inspect the current filtering capabilities and extend them for the new filter fields rather than implementing filtering logic from scratch.
- Entity type filtering should map to the underlying entity tables: `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`.
- Severity filtering applies only to advisory results. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field — use this for filtering.
- License filtering applies only to package results. The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a license field — use this for filtering.
- When a filter applies to a specific entity type (e.g., severity applies only to advisories), results of other entity types should be excluded from the response when that filter is active, or the filter should be ignored for non-applicable entity types. **Assumption pending clarification:** we assume filters narrow results to applicable entity types (e.g., specifying `severity=high` implicitly filters to advisory results only).
- Per the repository's key conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping. Use the `PaginatedResults<T>` response wrapper from `common/src/model/paginated.rs`.
- **Assumption pending clarification:** The specific filterable fields (entity type, severity, license) are assumptions based on the existing data model. The product owner should confirm which fields are most valuable to users.
- **Assumption pending clarification:** Comma-separated multi-value support and AND combination semantics are assumptions. The feature description does not specify filter UX behavior.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — existing shared filtering logic; extend for the new filter predicates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field used for severity filtering
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — contains the license field used for license filtering
- `modules/fundamental/src/advisory/endpoints/list.rs` — existing advisory list endpoint; inspect for filtering patterns to reuse
- `modules/fundamental/src/package/endpoints/list.rs` — existing package list endpoint; inspect for filtering patterns to reuse

## Acceptance Criteria
- [ ] The `GET /api/v2/search` endpoint accepts `type`, `severity`, and `license` query parameters
- [ ] Filtering by entity type correctly narrows results to the specified types
- [ ] Filtering by severity correctly narrows results to advisories with matching severity
- [ ] Filtering by license correctly narrows results to packages with matching license
- [ ] Multiple filter values can be combined (e.g., `type=sbom,advisory`)
- [ ] Filters combine with the search query using AND semantics
- [ ] Requesting with no filters returns all results (backward compatible)
- [ ] Invalid filter values return a clear error response

## Test Requirements
- [ ] Integration test verifying `type=sbom` returns only SBOM results
- [ ] Integration test verifying `type=advisory` returns only advisory results
- [ ] Integration test verifying `severity=high` returns only high-severity advisories
- [ ] Integration test verifying `license=MIT` returns only packages with MIT license
- [ ] Integration test verifying multiple filters combine correctly
- [ ] Integration test verifying backward compatibility — search without filters works as before
- [ ] Integration test verifying invalid filter values return appropriate error responses

## Verification Commands
- `cargo test -p tests --test search` — all search tests pass including new filter tests

## Dependencies
- Depends on: Task 1 — Optimize search query performance (indexes and query optimizations should be in place)
