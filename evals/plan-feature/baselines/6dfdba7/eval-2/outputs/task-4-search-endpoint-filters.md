## Repository
trustify-backend

## Description
Update the search REST endpoint to accept filter query parameters and expose relevance scores in the response. The endpoint at `GET /api/v2/search` currently accepts a search query but does not support structured filters. This task adds filter parameters to the endpoint, threads them through to the updated SearchService, and ensures the API response includes relevance information.

**Assumption (pending clarification):** The filter parameter naming convention is assumed to follow a bracket syntax (e.g., `?filter[severity]=critical`) since no API design specification was provided. This should be confirmed with the API design owner.

**Assumption (pending clarification):** It is assumed that only the unified search endpoint (`/api/v2/search`) needs filter support in this feature. Whether individual entity list endpoints (`/api/v2/sbom`, `/api/v2/advisory`, `/api/v2/package`) also need new filters is unspecified and excluded from this task.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameter extraction to the search handler; pass filters to SearchService; include relevance score in response serialization

## API Changes
- `GET /api/v2/search` — MODIFY: Accept new optional query parameters for filtering (e.g., `filter[entity_type]`, `filter[severity]`, `filter[date_from]`, `filter[date_to]`); response items now include an optional `relevance_score` field

## Implementation Notes
- The existing endpoint in `modules/search/src/endpoints/mod.rs` registers `GET /api/v2/search` — extend the handler's query parameter struct to include filter fields
- Use Axum's `Query<T>` extractor to deserialize filter parameters from the query string; define a `SearchFilterParams` struct with optional fields for each supported filter
- Pass the parsed filter parameters to the `SearchService` methods updated in Task 3
- The response type should extend or wrap the existing `PaginatedResults<T>` from `common/src/model/paginated.rs` to include a `relevance_score` field per item
- Follow the endpoint registration pattern from other modules, e.g., `modules/fundamental/src/sbom/endpoints/mod.rs` and `modules/fundamental/src/advisory/endpoints/mod.rs`
- Follow the error handling pattern: return `Result<T, AppError>` and use `.context()` for error wrapping as defined in `common/src/error.rs`
- Ensure backward compatibility: existing API consumers sending no filter parameters should receive the same behavior as before (unfiltered, but now relevance-ranked)

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — Pattern for list endpoints with query parameter extraction
- `modules/fundamental/src/advisory/endpoints/list.rs` — Pattern for list endpoints with filtering
- `common/src/model/paginated.rs::PaginatedResults<T>` — Response type to extend
- `common/src/error.rs::AppError` — Error handling pattern

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term` continues to work without filters (backward compatible)
- [ ] `GET /api/v2/search?q=term&filter[entity_type]=advisory` returns only advisory results
- [ ] `GET /api/v2/search?q=term&filter[severity]=critical` returns only results matching the severity filter
- [ ] Response items include a `relevance_score` field when a search query is provided
- [ ] Invalid filter parameter values return 400 Bad Request with a descriptive error message
- [ ] Endpoint is properly registered in the route configuration

## Test Requirements
- [ ] Integration test: search with no filters returns results from all entity types
- [ ] Integration test: search with entity_type filter returns only that entity type
- [ ] Integration test: search with date range filter returns only results within the range
- [ ] Integration test: search with invalid filter value returns 400 status
- [ ] Integration test: response includes relevance_score field for each result item

## Verification Commands
- `cargo test -p search` — Search module tests pass
- `cargo test --test search` — Search integration tests in tests/api/search.rs pass

## Dependencies
- Depends on: Task 3 — Improve SearchService with relevance scoring and filters
