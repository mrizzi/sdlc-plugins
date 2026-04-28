## Repository
trustify-backend

## Description
Add filtering capability to the search endpoint, allowing users to narrow search results by entity type, advisory severity, and date range. This addresses the MVP requirement "Add filters — some kind of filtering capability" from TC-9002. Filters are applied as query parameters on the existing `GET /api/v2/search` endpoint and combined using AND logic.

**Ambiguity note:** The feature description does not specify which fields should be filterable or how filters should be combined. This task assumes the MVP filter set is: entity type (sbom, advisory, package), severity (for advisories), and date range (created_after, created_before). This assumption is pending clarification from the product owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters (entity_type, severity, created_after, created_before) to the search endpoint handler and pass them to the service layer
- `modules/search/src/service/mod.rs` — Accept filter parameters in the search method and apply them as WHERE clause predicates alongside the full-text search query
- `common/src/db/query.rs` — Add shared filter predicate builders for date range and enum-based filtering if not already present

## Files to Create
- `modules/search/src/model/mod.rs` — Search filter model defining `SearchFilters` struct with optional fields: `entity_type: Option<EntityType>`, `severity: Option<String>`, `created_after: Option<DateTime>`, `created_before: Option<DateTime>`

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters: `entity_type` (enum: sbom, advisory, package), `severity` (string), `created_after` (ISO 8601 datetime), `created_before` (ISO 8601 datetime). When no filters are provided, behavior is unchanged (backward compatible).

## Implementation Notes
- The search endpoint is defined in `modules/search/src/endpoints/mod.rs` at `GET /api/v2/search`. Add the filter parameters as optional query parameters using Axum's `Query<T>` extractor.
- Create a `SearchFilters` struct in a new `modules/search/src/model/mod.rs` file following the module pattern used in `modules/fundamental/` (each domain module has `model/`, `service/`, `endpoints/`).
- In `modules/search/src/service/mod.rs`, modify the search method to accept `SearchFilters` and apply each non-None filter as an additional WHERE clause:
  - `entity_type`: filter which tables are queried (skip tables that don't match the requested type)
  - `severity`: apply only to advisory results, using the severity field from `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`)
  - `created_after` / `created_before`: apply as date range filter on the created timestamp column
- Use AND logic to combine all filters (all specified filters must match).
- Follow the existing query builder patterns in `common/src/db/query.rs` for filtering and pagination.
- Follow the existing error handling pattern: `Result<T, AppError>` with `.context()` wrapping.
- The response continues to use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- When `entity_type` filter is set to a specific type, results should only include that entity type. When not set, results include all entity types (current behavior).

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting; extend with date range and enum filter predicates
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper already used by the search endpoint
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct contains the severity field referenced by the severity filter
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of a list endpoint with query parameter extraction; reference for Axum `Query<T>` pattern

## Acceptance Criteria
- [ ] The `GET /api/v2/search` endpoint accepts optional `entity_type`, `severity`, `created_after`, and `created_before` query parameters
- [ ] When `entity_type=advisory` is specified, only advisory results are returned
- [ ] When `severity=critical` is specified, only advisories with critical severity are returned
- [ ] When `created_after` and `created_before` are specified, only results within the date range are returned
- [ ] Filters combine with AND logic (all specified filters must match)
- [ ] When no filters are provided, the endpoint behaves identically to its pre-filter behavior (backward compatible)
- [ ] Invalid filter values return an appropriate error response (400 Bad Request) using the `AppError` pattern
- [ ] A `SearchFilters` struct is defined in `modules/search/src/model/mod.rs`

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `entity_type=advisory` and `severity=critical` returns only critical advisories
- [ ] Integration test: search with `created_after` and `created_before` returns only results within the date range
- [ ] Integration test: search with multiple filters applied simultaneously (AND logic) returns correctly filtered results
- [ ] Integration test: search with no filters returns all entity types (backward compatibility)
- [ ] Integration test: search with an invalid `entity_type` value returns 400 Bad Request

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test` — all tests pass

## Dependencies
- Depends on: Task 2 — Optimize SearchService with full-text search and relevance ranking
