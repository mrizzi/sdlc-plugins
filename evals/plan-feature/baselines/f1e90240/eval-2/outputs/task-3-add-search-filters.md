## Repository

trustify-backend

## Target Branch

main

## Description

Add filtering capabilities to the `GET /api/v2/search` endpoint so that users can narrow search results by entity type, severity, date range, and other relevant fields. The feature requirement states "some kind of filtering capability" without specifying which filters to support.

This task adds query parameter-based filters to the search endpoint, leveraging the existing shared query builder infrastructure in `common/src/db/query.rs`.

**Assumptions (pending clarification):**
- **AMBIGUITY: Filter fields and types are unspecified.** The feature states "Add filters" with the note "Some kind of filtering capability" but does not specify which fields should be filterable, what filter operators to support (exact match, range, multi-select), or whether filters should be AND or OR combined. This task assumes the following initial filter set (pending stakeholder confirmation):
  - `entity_type`: filter by result type (sbom, advisory, package) -- exact match
  - `severity`: filter advisories by severity level -- exact match (leverages `severity` field on `AdvisorySummary`)
  - `date_from` / `date_to`: filter by creation/modification date -- range filter
  - `license`: filter packages by license type -- exact match (leverages `license` field on `PackageSummary`)
  - Filter combination uses AND logic (all specified filters must match)
- **AMBIGUITY: Interaction between filters and full-text search is undefined.** This task assumes filters are applied in conjunction with the search query (i.e., filters narrow the full-text search results, not replace them). Users can also use filters without a search query to browse/list filtered results.

## Acceptance Criteria

- [ ] `GET /api/v2/search` accepts optional query parameters for each supported filter
- [ ] Filters narrow the result set correctly when applied individually
- [ ] Multiple filters can be combined (AND logic) to further narrow results
- [ ] Filters work in conjunction with the full-text search query parameter
- [ ] Filters can be used without a search query to browse filtered results
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] The filtered results are still paginated using `PaginatedResults<T>`
- [ ] API documentation (if any) is updated to reflect new query parameters

## Files to Modify

- `modules/search/src/service/mod.rs` -- Extend `SearchService` to accept and apply filter parameters
- `modules/search/src/endpoints/mod.rs` -- Add filter query parameter parsing to the `GET /api/v2/search` handler
- `common/src/db/query.rs` -- Add or extend shared filter builder helpers for the new filter types if not already supported

## Implementation Notes

- Extend the search endpoint handler in `modules/search/src/endpoints/mod.rs` to parse filter query parameters from the request. The endpoint is registered at `GET /api/v2/search`.
- Use the shared query builder helpers in `common/src/db/query.rs` for constructing filter predicates. The existing infrastructure supports filtering, pagination, and sorting -- extend it with any new filter types (e.g., date range) if not already present.
- Filter on entity-specific fields by referencing the entity definitions: `entity/src/advisory.rs` has the advisory entity with severity data, `entity/src/package.rs` has the package entity, and `entity/src/sbom.rs` has the SBOM entity.
- The `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field for severity-based filtering. The `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` includes a `license` field for license-based filtering.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping. Invalid filter values should map to appropriate `AppError` variants using the patterns in `common/src/error.rs`.
- Filtered results must continue to use the `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs` for response formatting.
- Follow the endpoint registration pattern in `modules/search/src/endpoints/mod.rs` (route registration) consistent with how other module endpoints are structured (see `modules/fundamental/src/sbom/endpoints/mod.rs` for reference).

**Convention: Error handling** -- Applies: task modifies `modules/search/src/service/mod.rs`, `modules/search/src/endpoints/mod.rs`, and `common/src/db/query.rs` matching the convention's Rust service/endpoint/query scope. All handlers return `Result<T, AppError>` with `.context()` wrapping.

**Convention: Response types** -- Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint scope. List/filtered endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.

**Convention: Query helpers** -- Applies: task modifies `common/src/db/query.rs` matching the convention's database query scope. Shared filtering, pagination, and sorting helpers must be used and extended.

**Convention: Endpoint registration** -- Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope. Each module's `endpoints/mod.rs` registers routes; `server/main.rs` mounts all modules.

## Dependencies

- Task 1 (Optimize search performance) -- filters are applied to the optimized search queries
- Task 2 (Improve search relevance) -- filters work in conjunction with relevance-ranked results

## Test Requirements

- Add integration tests in `tests/api/search.rs` verifying each filter type narrows results correctly
- Add tests verifying that multiple filters combine with AND logic
- Add tests verifying that filters work with and without a search query
- Add tests verifying that invalid filter values return 400 Bad Request
- Add tests verifying that filtered results are paginated correctly
- Follow the existing integration test pattern using real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern
