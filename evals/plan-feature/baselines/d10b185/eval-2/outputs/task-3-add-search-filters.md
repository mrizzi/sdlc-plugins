# Task 3 — Add filter query parameters to search and list endpoints

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint (`GET /api/v2/search`) and relevant list endpoints. This addresses the "add filters" MVP requirement by allowing users to narrow search results by entity type, advisory severity, and date range.

**Assumption pending clarification:** The filter specification is assumed as follows since the feature description only says "some kind of filtering capability":
- **Entity type filter**: filter search results to a specific entity type (sbom, advisory, package)
- **Severity filter**: filter advisories by severity level (low, medium, high, critical)
- **Date range filter**: filter SBOMs and advisories by ingestion/publication date range (from/to)

These filters should be combinable (AND logic). Confirm the exact filter set with the product owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to `GET /api/v2/search` (entity_type, severity, date_from, date_to)
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept and apply filter criteria to search queries
- `modules/fundamental/src/advisory/endpoints/list.rs` — add severity filter query parameter to `GET /api/v2/advisory`
- `modules/fundamental/src/sbom/endpoints/list.rs` — add date range filter query parameters to `GET /api/v2/sbom`
- `common/src/db/query.rs` — add shared filter helper functions for severity enum filtering and date range filtering if not already present

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom|advisory|package), `severity` (enum: low|medium|high|critical), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date)
- `GET /api/v2/advisory` — MODIFY: add optional query parameter `severity` (enum: low|medium|high|critical)
- `GET /api/v2/sbom` — MODIFY: add optional query parameters `date_from` (ISO 8601 date), `date_to` (ISO 8601 date)

## Implementation Notes
- Use the existing query builder helpers in `common/src/db/query.rs` for shared filtering logic. The file already provides filtering, pagination, and sorting utilities — extend it with:
  1. A severity filter function that accepts an optional severity enum and applies a `WHERE severity = $1` condition.
  2. A date range filter function that accepts optional `date_from`/`date_to` parameters and applies `WHERE created_at >= $1 AND created_at <= $2` conditions.
- For the entity type filter on the search endpoint, apply it in `SearchService` by conditionally joining/querying only the specified entity table(s) instead of all three.
- Follow the existing endpoint parameter pattern in `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/sbom/endpoints/list.rs` — these already accept query parameters for pagination and sorting. Add the new filter parameters to the same `Query` extractor struct.
- The severity field exists on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`). Use this field for the severity filter.
- The license field exists on `PackageSummary` (see `modules/fundamental/src/package/model/summary.rs`). This is not needed for MVP filters but is noted for future filter expansion.
- All filter parameters must be optional — when omitted, no filtering is applied (backward compatible).
- Error handling: return `400 Bad Request` via `AppError` for invalid filter values (e.g., unknown severity level, malformed dates).
- Per `docs/constraints.md` section 5 (Code Change Rules): reuse existing query helpers in `common/src/db/query.rs` rather than duplicating filter logic in each endpoint.
- Per `docs/constraints.md` section 2 (Commit Rules): commits must reference TC-9002 and follow Conventional Commits.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder with existing filtering and pagination support; extend rather than duplicate
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper already used by all list endpoints
- `modules/fundamental/src/advisory/endpoints/list.rs` — existing list endpoint with query parameter extraction; follow its pattern for adding new filter parameters
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing list endpoint; follow same pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the `severity` field used for the severity filter

## Acceptance Criteria
- [ ] `GET /api/v2/search` accepts optional `entity_type`, `severity`, `date_from`, and `date_to` query parameters
- [ ] `GET /api/v2/advisory` accepts an optional `severity` query parameter that filters results by advisory severity
- [ ] `GET /api/v2/sbom` accepts optional `date_from` and `date_to` query parameters that filter results by date range
- [ ] All filter parameters are optional — omitting them returns unfiltered results (backward compatible)
- [ ] Filters combine with AND logic — specifying multiple filters narrows results
- [ ] Invalid filter values return `400 Bad Request` with a descriptive error message
- [ ] Existing API consumers are not broken — all current request formats continue to work

## Test Requirements
- [ ] Add integration tests in `tests/api/search.rs` for search with entity_type filter (returns only matching entity types)
- [ ] Add integration tests in `tests/api/search.rs` for search with severity filter (returns only advisories matching the severity)
- [ ] Add integration tests in `tests/api/search.rs` for search with date range filter
- [ ] Add integration tests in `tests/api/search.rs` for combined filters (e.g., entity_type + severity)
- [ ] Add integration tests in `tests/api/advisory.rs` for advisory list with severity filter
- [ ] Add integration tests in `tests/api/sbom.rs` for SBOM list with date range filter
- [ ] Add test for invalid filter values returning 400 Bad Request
- [ ] Verify all existing integration tests in `tests/api/search.rs`, `tests/api/advisory.rs`, and `tests/api/sbom.rs` continue to pass

## Verification Commands
- `cargo test --test api search` — all search tests pass including new filter tests
- `cargo test --test api advisory` — advisory list tests pass including severity filter
- `cargo test --test api sbom` — SBOM list tests pass including date range filter

## Documentation Updates
- `README.md` — document new filter query parameters for search and list endpoints if the README covers API usage

## Dependencies
- Depends on: Task 2 — Optimize SearchService with full-text search and relevance ranking
