# Task 3: Add Filter Query Parameters to Search Endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Extend the `GET /api/v2/search` endpoint to accept filter query parameters, enabling users to narrow search results by entity type, severity, and date range. This involves modifying the endpoint handler in `modules/search/src/endpoints/mod.rs` to parse new query parameters and extending the shared query builder in `common/src/db/query.rs` with filter-application helpers that translate these parameters into SQL `WHERE` clauses.

**Ambiguity note:** The feature description (TC-9002) states "Some kind of filtering capability" without specifying which fields should be filterable, how filters combine, or whether filters apply to the unified search endpoint or per-entity list endpoints. The following assumptions are made pending product owner clarification.

**Assumption (pending clarification):** Filter parameters target the unified `GET /api/v2/search` endpoint only (not individual entity list endpoints). The following filters are implemented:
- `entity_type` — Restrict results to a specific entity kind: `sbom`, `advisory`, or `package`. Accepts a single value.
- `severity` — Filter advisory results by severity level (e.g., `critical`, `high`, `medium`, `low`). Only meaningful when results include advisories; ignored for other entity types.
- `created_after` / `created_before` — ISO 8601 date strings that constrain results to a creation date range.

**Assumption (pending clarification):** Filters combine with AND semantics. If `entity_type=advisory` and `severity=critical` are both provided, only critical advisories are returned. There is no OR combinator in this iteration.

**Assumption (pending clarification):** Unknown or unsupported filter parameter values (e.g., `severity=unknown_level`) return a `400 Bad Request` with a descriptive error message rather than silently ignoring the value.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add a `SearchFilterParams` struct (deserialized from query string via `axum::extract::Query`) with optional fields for `entity_type`, `severity`, `created_after`, and `created_before`. Pass parsed filters to the search service.
- `common/src/db/query.rs` — Add helper functions to apply filter predicates to a SeaORM `Select` query:
  - `apply_entity_type_filter()` — Adds a `WHERE entity_type = ?` clause
  - `apply_severity_filter()` — Adds a `WHERE severity = ?` clause for advisory results
  - `apply_date_range_filter()` — Adds `WHERE created_at >= ?` and/or `WHERE created_at <= ?` clauses
- `modules/search/src/service/mod.rs` — Update `SearchService` query construction to accept and apply the filter parameters when building the database query

## Implementation Notes
- Define the `SearchFilterParams` struct in `modules/search/src/endpoints/mod.rs` using `#[derive(Deserialize)]` with `serde` and `#[serde(default)]` so all filter fields are optional. Use `Option<String>` for `entity_type` and `severity`, and `Option<chrono::NaiveDate>` (or `Option<String>` with manual parsing) for date range fields.
- The endpoint handler should extract `Query<SearchFilterParams>` alongside any existing query parameters (e.g., search query `q`, pagination). The Axum framework supports multiple `Query` extractors or a combined struct.
- In `common/src/db/query.rs`, follow the existing pattern of helper functions that take a mutable `SelectStatement` or `Select<E>` and apply conditions. The existing query builder already handles pagination and sorting; filter helpers should compose with those.
- For `entity_type` filtering: the search service likely queries multiple tables (sbom, advisory, package) and unions the results. When `entity_type` is specified, skip querying the irrelevant tables entirely rather than filtering post-query. This is more efficient and avoids unnecessary database work.
- For `severity` filtering: the `severity` field exists on the Advisory entity (see `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` includes a severity field). Apply this filter only to the advisory subquery. If `entity_type` is set to a non-advisory type and `severity` is also provided, return a `400 Bad Request` indicating the combination is invalid.
- For date range filtering: apply `created_at >= created_after` and `created_at <= created_before` predicates. Both are optional and independent. Validate that `created_after` is not after `created_before` if both are provided (return `400` if invalid).
- All error responses should use the `AppError` enum from `common/src/error.rs` with `.context()` wrapping per project conventions.
- Per CONVENTIONS.md: endpoint handlers return `Result<T, AppError>`, query helpers live in `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint module scope.
  Applies: task modifies `common/src/db/query.rs` matching the convention's shared query helper scope.

## Reuse Candidates
- `common/src/db/query.rs` — Existing filtering/pagination/sorting helpers to follow as patterns for the new filter functions
- `modules/fundamental/src/advisory/endpoints/list.rs` — Reference for how list endpoints parse query parameters in this project
- `modules/fundamental/src/advisory/model/summary.rs` — Severity field type definition for consistent enum usage
- `common/src/error.rs` — `AppError` enum for consistent error response handling

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` filters results to critical-severity advisories
- [ ] `GET /api/v2/search?created_after=2024-01-01&created_before=2024-06-30` returns only results within the date range
- [ ] Filters combine with AND semantics: `entity_type=advisory&severity=high` returns only high-severity advisories
- [ ] Invalid filter combinations (e.g., `entity_type=sbom&severity=critical`) return `400 Bad Request`
- [ ] Invalid date ranges (`created_after` > `created_before`) return `400 Bad Request`
- [ ] Omitting all filter parameters returns unfiltered results (backwards compatible)
- [ ] Project compiles without errors

## Test Requirements
- [ ] Unit tests for each filter helper function in `common/src/db/query.rs` validating correct SQL predicate generation
- [ ] Integration test: search with `entity_type` filter returns only the specified entity type
- [ ] Integration test: search with `severity` filter returns only matching advisories
- [ ] Integration test: search with date range filters returns only results within the range
- [ ] Integration test: combined filters narrow results correctly
- [ ] Integration test: invalid filter values return `400` status code
- [ ] Regression: existing search tests in `tests/api/search.rs` continue to pass without modification

## Dependencies
- Depends on: Task 2 — Update entities with search vector columns (entity definitions must include the fields referenced by filter logic)

---

`[sdlc-workflow] Description digest: sha256-md:c4e82f6a1d3b9057e2a8f4c6d91b73e5a0f28d4c6e1a3b597f0d2e4a6c8b1f3d`
