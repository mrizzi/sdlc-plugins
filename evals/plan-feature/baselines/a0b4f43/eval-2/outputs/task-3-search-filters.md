## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow search results by entity type, advisory severity, and date range. This addresses the TC-9002 requirement to "add filters" with "some kind of filtering capability." The filters are implemented as optional query parameters on the existing search endpoint.

**Assumption (pending clarification):** The specific filters (entity type, severity, date range) are assumed based on the existing data model. The product owner should confirm which filters are most valuable and whether additional filters (e.g., license type for packages, SBOM format) are needed.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add filter parameters to the search method, applying them as WHERE clause conditions alongside the full-text search
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter values (entity type, severity, date range) on `GET /api/v2/search`

## Files to Create
- `modules/search/src/model/filters.rs` — Filter parameter structs: `SearchFilters` with optional fields for entity_type (enum), severity (string), date_from (DateTime), date_to (DateTime)

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `entity_type` (enum: sbom|advisory|package), `severity` (string matching advisory severity values), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). All parameters are optional; when omitted, no filtering is applied (backward-compatible).

## Implementation Notes
- Define a `SearchFilters` struct with optional fields for each filter dimension. Use `Option<T>` for each field so that omitting a filter means "no constraint."
- For entity type filtering: when `entity_type` is specified, only query the matching entity table instead of all three. This also improves performance for type-scoped searches.
- For severity filtering: apply a WHERE clause on the `severity` field of the `advisory` table. This filter only applies when searching advisories (either explicitly via entity_type=advisory or when returning mixed results).
- For date range filtering: apply WHERE clauses on creation/modification timestamp fields. Use `>=` for `date_from` and `<=` for `date_to`.
- Follow the existing endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter extraction using Axum extractors.
- Follow the existing query helper patterns in `common/src/db/query.rs` for building filter conditions.
- Ensure filter parameters are validated: invalid enum values return a 400 Bad Request, invalid date formats return a 400 Bad Request with a descriptive error message.
- Per docs/constraints.md §5.4: Reuse existing query builder helpers from `common/src/db/query.rs` for filtering logic rather than writing custom filter builders.
- Per docs/constraints.md §2.1-2.3: Commits must reference TC-9002, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers that likely include filtering patterns to reuse
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of query parameter extraction for list endpoints
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct showing the severity field type and values
- `modules/fundamental/src/package/model/summary.rs` — PackageSummary struct showing available fields for potential future filters

## Acceptance Criteria
- [ ] Search endpoint accepts optional `entity_type` query parameter and filters results to the specified type
- [ ] Search endpoint accepts optional `severity` query parameter and filters advisory results by severity
- [ ] Search endpoint accepts optional `date_from` and `date_to` query parameters for date range filtering
- [ ] All filter parameters are optional — omitting them returns unfiltered results (backward-compatible)
- [ ] Invalid filter values (unknown entity type, malformed date) return 400 Bad Request with a descriptive error
- [ ] Filters compose correctly with full-text search (filters narrow, search ranks)
- [ ] Multiple filters can be combined in a single request

## Test Requirements
- [ ] Test filtering by each entity type individually (sbom, advisory, package)
- [ ] Test severity filtering returns only advisories matching the specified severity
- [ ] Test date range filtering with both bounds, only start date, and only end date
- [ ] Test that filters compose with full-text search correctly
- [ ] Test that invalid filter values return 400 status codes
- [ ] Test that omitting all filters returns the same results as before (backward compatibility)
- [ ] Test combining multiple filters in a single request

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test api search` — search integration tests pass

## Dependencies
- Depends on: Task 2 — Search service ranking (the filters build on top of the refactored search service)
