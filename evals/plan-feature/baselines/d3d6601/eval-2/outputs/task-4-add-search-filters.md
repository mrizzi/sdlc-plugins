## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint, allowing users to narrow search results by entity-specific attributes. This addresses the TC-9002 MVP requirement "Add filters."

**Ambiguity note:** The feature description says "some kind of filtering capability" without specifying which fields to filter on, what filter types to support (exact match, range, multi-select), or how filters should compose (AND vs OR). **Assumption pending clarification:** We implement the following filters based on the entity model analysis:
- **Severity filter** (for advisories): exact match or multi-select on severity values (e.g., `?severity=critical,high`)
- **License filter** (for packages): exact match on license identifier (e.g., `?license=MIT`)
- **Date range filter** (for SBOMs): range filter on creation/ingestion date (e.g., `?date_from=2024-01-01&date_to=2024-12-31`)
- **Entity type filter**: filter results to a specific entity type (e.g., `?type=advisory`)

Filters compose with AND logic (all specified filters must match). These filter choices should be validated with the product owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add query parameter extraction for filter fields (severity, license, date_from, date_to, type); pass filter parameters to SearchService
- `modules/search/src/service/mod.rs` — extend search method to accept and apply filter parameters alongside full-text search; use filter composition helpers from `common/src/db/query.rs`

## Files to Create
- `modules/search/src/model/mod.rs` — define `SearchFilters` struct to encapsulate filter parameters (severity, license, date_from, date_to, entity_type) with optional fields

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `severity` (string, comma-separated), `license` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date), `type` (string enum: sbom, advisory, package)

## Implementation Notes
- Inspect the existing endpoint handler in `modules/search/src/endpoints/mod.rs` to understand how query parameters are currently extracted — follow the same deserialization pattern (likely Axum `Query<T>` extractor)
- Reference how list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` handle query parameters for pagination and filtering — apply the same patterns
- Use the filter composition helpers added in Task 3 (`apply_filter`, `compose_filters`) from `common/src/db/query.rs` to build the filter predicates
- The `severity` field exists on `AdvisorySummary` (per `modules/fundamental/src/advisory/model/summary.rs`) — use this for severity filtering
- The `license` field exists on `PackageSummary` (per `modules/fundamental/src/package/model/summary.rs`) — use this for license filtering
- For entity type filtering, apply the filter at the query level by including/excluding the UNION branches for each entity type rather than filtering after combining
- Follow the model pattern from `modules/fundamental/src/sbom/model/mod.rs` for the new `SearchFilters` struct
- Per docs/constraints.md §2 (Commit Rules): use Conventional Commits format with Jira issue ID in footer
- Per docs/constraints.md §5.4: reuse the query builder helpers from `common/src/db/query.rs` added in Task 3

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers including the new filter composition helpers from Task 3
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of query parameter handling in a list endpoint
- `modules/fundamental/src/advisory/endpoints/list.rs` — example of query parameter handling with filtering
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with severity field, reference for filter field types
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` struct with license field, reference for filter field types

## Acceptance Criteria
- [ ] `GET /api/v2/search?severity=critical` returns only advisory results with critical severity
- [ ] `GET /api/v2/search?license=MIT` returns only package results with MIT license
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only SBOM results within the date range
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] Multiple filters compose with AND logic: `?severity=critical&type=advisory` returns only critical advisories
- [ ] Filters work in combination with the search query: `?q=openssl&severity=high` searches for "openssl" among high-severity advisories
- [ ] Invalid filter values return a 400 Bad Request with a descriptive error message
- [ ] Omitting all filters returns unfiltered search results (backward compatible)

## Test Requirements
- [ ] Integration test: search with severity filter returns only matching advisories
- [ ] Integration test: search with license filter returns only matching packages
- [ ] Integration test: search with date range filter returns only SBOMs within range
- [ ] Integration test: search with entity type filter returns only matching entity types
- [ ] Integration test: multiple filters compose correctly with AND logic
- [ ] Integration test: filters combined with search query work correctly
- [ ] Integration test: invalid filter values return 400 status
- [ ] Integration test: no filters returns full (unfiltered) search results
- [ ] Existing search tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test api search` — search integration tests pass
- `cargo test --test api` — all integration tests pass

## Dependencies
- Depends on: Task 2 — Refactor SearchService for full-text search (filters build on the refactored search service)
- Depends on: Task 3 — Add query builder full-text helpers (filters use the composition helpers)

[sdlc-workflow] Description digest: sha256:c5abc42004e57c2ae1e5d11204a1d3b13abcbbc204ba3a11f5491beffd8717d7
