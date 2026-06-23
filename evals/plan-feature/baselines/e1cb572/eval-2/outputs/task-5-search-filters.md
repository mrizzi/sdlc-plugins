# Task 5: Add Filter Parameters to Search Endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add query parameter filters to the `GET /api/v2/search` endpoint to allow users to narrow search results by entity type, severity (for advisories), and date range. This addresses the MVP requirement "Add filters — Some kind of filtering capability."

**Ambiguity note:** The feature says "some kind of filtering capability" with no specification of which filters. This task assumes the following filters based on available entity fields (pending product owner clarification):
- `type` — filter by entity type (sbom, advisory, package)
- `severity` — filter advisories by severity level (uses `AdvisorySummary.severity` field)
- `created_after` / `created_before` — filter by creation date range

These are **assumptions** based on the data model. The product owner should confirm which filters are most valuable to users.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters (`type`, `severity`, `created_after`, `created_before`) to the `GET /api/v2/search` handler. Parse and validate filter values, pass them to `SearchService`.
- `modules/search/src/service/mod.rs` — Update the search method signature to accept optional filter parameters. Apply filters to the database query using helpers from `common/src/db/query.rs`.

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters:
  - `type` (string, optional): Filter by entity type. Values: `sbom`, `advisory`, `package`.
  - `severity` (string, optional): Filter advisory results by severity. Values: `low`, `medium`, `high`, `critical`.
  - `created_after` (ISO 8601 date, optional): Return only results created after this date.
  - `created_before` (ISO 8601 date, optional): Return only results created before this date.

## Implementation Notes
- Use Axum's `#[derive(Deserialize)]` on a query parameter struct to parse filter values from the URL. Follow the pattern used in existing list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs`.
- The `type` filter determines which entity tables to query. If `type=advisory`, only query the advisory table. If omitted, query all entity types (current behavior).
- The `severity` filter only applies when searching advisories. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` has a severity field — use the same enum/type for filter validation.
- Date range filters should use the existing filtering helpers in `common/src/db/query.rs` to add `WHERE created_at >= ? AND created_at <= ?` clauses.
- Invalid filter values should return a `400 Bad Request` with a descriptive error message via `AppError`.
- Per CONVENTIONS.md: use the existing query builder helpers for filtering.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing filtering helpers for date range and equality filters
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for how list endpoints accept query parameters via Axum extractors
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Severity field type/enum for filter validation
- `common/src/error.rs::AppError` — Error response for invalid filter values

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?severity=critical` filters advisory results by severity
- [ ] `GET /api/v2/search?created_after=2024-01-01` filters results by creation date
- [ ] Filters can be combined: `?q=openssl&type=advisory&severity=high`
- [ ] Invalid filter values return `400 Bad Request` with a descriptive error
- [ ] Omitting all filters preserves existing behavior (search all entity types)

## Test Requirements
- [ ] Integration test: filter by entity type returns only that type
- [ ] Integration test: filter by severity returns only matching advisories
- [ ] Integration test: date range filter returns only results within range
- [ ] Integration test: combined filters narrow results correctly
- [ ] Integration test: invalid filter value returns 400 status

## Dependencies
- Depends on: Task 4 — Implement full-text search with relevance ranking in SearchService

---

`[sdlc-workflow] Description digest: sha256-md:e6a0b4c8d3f95e1a2b7c4d9f8e0a3b5c7d9f1a3c5e7b9d0f2a4c6e8b1d3f5a7`
