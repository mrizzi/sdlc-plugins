## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint (GET /api/v2/search) so that users can narrow search results by entity type and search scope. Currently the search endpoint performs unfiltered full-text search across all entities. This task adds query parameters for entity type filtering (SBOM, advisory, package) and a qualifier parameter to restrict which fields are searched.

**Ambiguity note:** The feature description (TC-9002) specifies "some kind of filtering capability" without defining which filters. This task assumes entity type and search scope qualifiers as the initial filter set, pending clarification from the feature owner.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters (entity type, search qualifier) to the GET /api/v2/search handler
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter parameters when building search queries
- `common/src/db/query.rs` — add filter builder helpers for entity type filtering if not already covered by existing helpers
- `tests/api/search.rs` — add integration tests for filtered search queries

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom, advisory, package) and `qualifier` (string, restricts search to specific fields)

## Implementation Notes
Follow the existing module pattern in `modules/search/`: the endpoint layer (`endpoints/mod.rs`) handles HTTP concerns (parsing query parameters, returning responses), and the service layer (`service/mod.rs`) handles business logic (building and executing queries).

For the filter query parameters, define a struct (e.g., `SearchFilter`) with optional fields for `entity_type` and `qualifier`. Use Axum's `Query` extractor to parse filter parameters from the request URL, consistent with how other endpoints in the codebase handle query parameters (see `modules/fundamental/src/sbom/endpoints/list.rs` for an example of list endpoint parameter handling).

Use the shared query builder helpers in `common/src/db/query.rs` for constructing filtered queries. The existing filtering and pagination utilities should be extended or composed to support the new filter dimensions. Follow the same patterns used for SBOM and advisory list endpoints.

Return results using `PaginatedResults<T>` from `common/src/model/paginated.rs`, consistent with all other list endpoints.

All handlers must return `Result<T, AppError>` with `.context()` wrapping for error handling, per the established error handling pattern (see `common/src/error.rs`).

Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the search module.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` handler file scope.

Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` endpoint file scope.

Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — existing filtering, pagination, and sorting utilities that should be composed or extended for search filters rather than writing new query construction logic
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of a list endpoint with query parameter parsing that can serve as a pattern for the search filter parameters
- `common/src/model/paginated.rs::PaginatedResults<T>` — the standard response wrapper for list endpoints; reuse for filtered search results

## Acceptance Criteria
- [ ] GET /api/v2/search accepts an optional `entity_type` query parameter that filters results to only the specified entity type (sbom, advisory, or package)
- [ ] GET /api/v2/search accepts an optional `qualifier` query parameter that restricts which fields are searched
- [ ] When no filter parameters are provided, the endpoint behaves identically to the current implementation (backward compatible)
- [ ] Invalid filter values return an appropriate error response with a meaningful message
- [ ] All existing search tests continue to pass without modification

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `entity_type=advisory` returns only advisory results
- [ ] Integration test: search with `entity_type=package` returns only package results
- [ ] Integration test: search with no filters returns results across all entity types (backward compatibility)
- [ ] Integration test: search with an invalid `entity_type` value returns an appropriate error response
- [ ] Integration test: search with combined `entity_type` and `qualifier` parameters returns correctly scoped results
