# Task 3 — Add Search Filter Parameters

## Repository
trustify-backend

## Description
Add filtering capabilities to the search endpoint so users can narrow results by entity type (SBOM, advisory, package), severity level (for advisories), and date range. This addresses the MVP requirement for "some kind of filtering capability" with the most useful domain-specific filters.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to `GET /api/v2/search` (entity_type, severity, date_from, date_to)
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept and apply filter criteria to search queries
- `common/src/db/query.rs` — add filter builder helpers for entity type, severity, and date range filtering if not already present

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom, advisory, package), `severity` (enum matching advisory severity values), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date)

## Implementation Notes
- Inspect the existing endpoint in `modules/search/src/endpoints/mod.rs` to understand the current query parameter structure. New filter parameters must be additive (optional) to maintain backward compatibility.
- Use the existing filtering patterns from `common/src/db/query.rs` as the foundation. The shared query builder already supports filtering and pagination — extend it with the new filter types rather than creating separate filter logic.
- For entity type filtering: when `entity_type` is specified, restrict the search to only that entity's table. When absent, search across all entities (current behavior).
- For severity filtering: use the `severity` field from `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs`). This filter only applies when searching advisories.
- For date range filtering: filter on created/modified timestamps. Use standard SeaORM `between` or `gte`/`lte` conditions.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the project's error handling convention (see `common/src/error.rs`).
- Per constraints doc 5.4: reuse existing query builder helpers from `common/src/db/query.rs` rather than duplicating filter logic.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers to extend
- `common/src/error.rs` — `AppError` enum for error handling pattern
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field to reference for severity filter values
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of list endpoint with query parameters to follow as a pattern

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory&severity=critical` returns only critical advisories
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] Multiple filters can be combined in a single request
- [ ] Omitting all filters returns the same results as before (backward compatibility)
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Test filtering by each entity type individually (sbom, advisory, package)
- [ ] Test severity filter with valid and invalid values
- [ ] Test date range filtering with various combinations (from only, to only, both)
- [ ] Test combining multiple filters simultaneously
- [ ] Test that invalid filter parameters return 400 Bad Request with descriptive error messages
- [ ] Test backward compatibility: request without filters returns expected results

## Dependencies
- Depends on: Task 2 — Extend SearchService with Full-Text Ranking (search service infrastructure must be in place)
