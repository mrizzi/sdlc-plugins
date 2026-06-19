# Task 3: Add Filter Parameters to Search Endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the search API endpoint (GET /api/v2/search) to accept filter query parameters, allowing users to narrow search results by entity type, advisory severity, and date range. This addresses the TC-9002 requirement "Add filters — some kind of filtering capability."

**Ambiguity: "Add filters" — "Some kind of filtering capability"** — The feature does not specify which fields should be filterable, what filter operators are needed (exact match, range, multi-select), or how filters interact with full-text search. This task assumes a practical set of filters based on the existing entity model fields.

**Assumption (A2)**: The filter parameters implemented are:
- `type` — filter by entity type: `sbom`, `advisory`, `package` (multi-select, comma-separated)
- `severity` — filter advisories by severity level (e.g., `critical`, `high`, `medium`, `low`)
- `date_from` / `date_to` — filter results by creation/publication date range (ISO 8601)

These assumptions are pending confirmation from the product owner. Additional filters (e.g., license type for packages, vendor/supplier for SBOMs) may be needed.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for `type`, `severity`, `date_from`, `date_to` using Axum's `Query<SearchFilters>` extractor; pass filters to the search service
- `modules/search/src/service/mod.rs` — Accept a `SearchFilters` struct parameter; apply filter conditions to the full-text search query (combine tsvector match with WHERE clauses for filters)
- `common/src/db/query.rs` — Add filter-building helpers for enum-based filtering (severity) and date range filtering, extending the existing shared query builder patterns

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchFilters` struct (deserializable from query parameters) and `SearchEntityType` enum; define `SearchResultItem` if not already present

## Implementation Notes
- The existing endpoint at `modules/search/src/endpoints/mod.rs` (GET /api/v2/search) currently accepts a query string parameter. Extend it with additional optional query parameters using Axum's `Query<T>` extractor pattern, following the approach used in list endpoints like `modules/fundamental/src/sbom/endpoints/list.rs`
- Define a `SearchFilters` struct with `#[derive(Deserialize)]` containing:
  ```rust
  pub struct SearchFilters {
      pub q: Option<String>,           // search query text
      pub r#type: Option<String>,      // comma-separated entity types
      pub severity: Option<String>,    // advisory severity filter
      pub date_from: Option<String>,   // ISO 8601 date
      pub date_to: Option<String>,     // ISO 8601 date
  }
  ```
- When `type` filter is provided, the search service should only query the specified entity tables (e.g., if `type=sbom`, skip advisory and package tables)
- Severity filter applies only to advisory results — if the user searches with `severity=critical` and `type=sbom`, severity filter is silently ignored for SBOM results (or returns advisory results only — behavior should be documented)
- Date range filters use `created_at >= date_from AND created_at <= date_to` conditions
- Follow the existing filtering pattern in `common/src/db/query.rs` which provides shared query builder helpers for filtering, pagination, and sorting
- All filter parameters are optional — omitting a filter means no restriction on that dimension
- Error handling follows `Result<T, AppError>` with `.context()` wrapping for invalid filter values (e.g., unparseable date)
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field that can be used for filtering
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a license field that could be added as a future filter

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `type` query parameter to filter by entity type
- [ ] GET /api/v2/search accepts optional `severity` query parameter to filter advisory results by severity
- [ ] GET /api/v2/search accepts optional `date_from` and `date_to` query parameters for date range filtering
- [ ] All filter parameters are optional and can be combined with the search query
- [ ] Omitting all filters returns unfiltered search results (backward compatible)
- [ ] Invalid filter values (e.g., invalid date format, unknown entity type) return 400 Bad Request with a descriptive error message
- [ ] Filter parameters are documented in the endpoint (for OpenAPI/Swagger generation if applicable)
- [ ] Search results with filters still return `PaginatedResults<T>` and maintain relevance ordering from Task 2

## Test Requirements
- [ ] Integration test: search with `type=sbom` returns only SBOM results
- [ ] Integration test: search with `type=advisory&severity=critical` returns only critical advisories
- [ ] Integration test: search with `date_from` and `date_to` returns only results within the date range
- [ ] Integration test: search with multiple filters combined (type + severity + date range) returns correctly filtered results
- [ ] Integration test: search with no filters returns all matching results (backward compatibility)
- [ ] Integration test: search with invalid date format returns 400 status
- [ ] Integration test: search with unknown entity type returns 400 status
- [ ] Tests in `tests/api/search.rs` following the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Dependencies
- Depends on: Task 2 — Full-Text Search Service with Relevance Ranking (filter logic builds on top of the refactored search service)

## Conventions

- **Error handling**: Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's `Result<T, AppError>` with `.context()` scope.
- **Response types**: Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `PaginatedResults<T>` scope.
- **Query helpers**: Applies: task modifies `common/src/db/query.rs` matching the convention's shared filtering/pagination/sorting scope.
- **Testing**: Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope.
