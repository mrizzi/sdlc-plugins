## Repository
trustify-backend

## Target Branch
main

## Description
Add query parameter-based filters to the `GET /api/v2/search` endpoint, enabling users to narrow search results by entity type, advisory severity, and package license. This addresses the MVP requirement "Add filters" by extending the search endpoint with optional filter parameters that compose with the existing full-text search query. All filters are optional and AND-combined when multiple are provided.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept and apply filter criteria (entity type, severity, license) to the search query
- `modules/search/src/endpoints/mod.rs` — add query parameter extraction for filter fields (`type`, `severity`, `license`) and pass them to `SearchService`

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `type` (enum: sbom, advisory, package), `severity` (string, e.g., "critical", "high", "medium", "low"), `license` (string, partial match). All filters are optional and combinable with AND logic. Response shape remains unchanged (`PaginatedResults`).

## Implementation Notes
Extend the search endpoint in `modules/search/src/endpoints/mod.rs` to parse additional optional query parameters:
- `type`: filters results to a specific entity type (sbom, advisory, package). This should filter at the query level, not post-query, to maintain pagination accuracy.
- `severity`: filters advisory results by severity field (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` which includes a severity field). Non-advisory results should be excluded when this filter is active.
- `license`: filters package results by license field (see `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` which includes a license field). Non-package results should be excluded when this filter is active.

In `modules/search/src/service/mod.rs`, add filter application logic:
1. Accept a filter struct (or individual filter parameters) alongside the search query.
2. Build conditional WHERE clauses using the shared query builder pattern from `common/src/db/query.rs`. The existing `query.rs` provides filtering helpers — extend or compose with these rather than building raw SQL.
3. Ensure filters compose correctly with full-text search: the WHERE clause should AND the tsvector match with any active filters.
4. When entity-type-specific filters (severity, license) are active, automatically scope results to the relevant entity type.

Follow the error handling pattern using `Result<T, AppError>` from `common/src/error.rs` with `.context()` wrapping for any new error paths.

Per constraints (docs/constraints.md):
- Commit messages must follow Conventional Commits and reference TC-9002 (§2.1, §2.2).
- Include `--trailer="Assisted-by: Claude Code"` on all commits (§2.3).
- Keep changes scoped to the files listed (§5.1).
- Do not duplicate query building logic — reuse `common/src/db/query.rs` helpers (§5.4).

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend these for the new filter parameters rather than building custom filtering logic
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct containing the `severity` field to filter on
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct containing the `license` field to filter on
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of a list endpoint with query parameter handling; follow the same pattern for adding filter parameters

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?license=MIT` returns only packages matching the MIT license
- [ ] Filters combine with the search query: `GET /api/v2/search?q=openssl&type=advisory` returns only advisories matching "openssl"
- [ ] Multiple filters combine with AND logic: `GET /api/v2/search?q=openssl&type=advisory&severity=high` narrows results further
- [ ] Omitting all filters preserves existing behavior (all entity types, no severity/license filtering)
- [ ] Pagination works correctly with filters applied (total count reflects filtered result set)
- [ ] Invalid filter values return a 400 error with a descriptive message

## Test Requirements
- [ ] Integration test: filter by entity type returns only that entity type
- [ ] Integration test: filter by severity returns only advisories with matching severity
- [ ] Integration test: filter by license returns only packages with matching license
- [ ] Integration test: combining multiple filters narrows results correctly (AND logic)
- [ ] Integration test: filters compose with full-text search query
- [ ] Integration test: invalid filter value (e.g., `type=unknown`) returns 400 status
- [ ] Integration test: no filters returns results from all entity types (backward compatibility)

## Dependencies
- Depends on: Task 2 — Search relevance ranking (filters build on the refactored SearchService with full-text search)

[sdlc-workflow] Description digest: sha256:01be2819c556f56e659518385ac90860e9e6dd9a23d586934e7077345e5f473c
