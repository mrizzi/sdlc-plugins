# Task 5 — Add Filter Parameters to Search Endpoint

## Repository
trustify-backend

## Description
Extend the `GET /api/v2/search` endpoint in `modules/search/src/endpoints/mod.rs` to accept filter query parameters (entity type, severity, date range, license) and pass them through to the updated `SearchService`. This exposes the new filtering capabilities to API consumers.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter extraction for filter fields (entity_type, severity, date_from, date_to, license) and pass them to `SearchService`

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `entity_type` (string: "sbom"|"advisory"|"package"), `severity` (string), `date_from` (ISO 8601 datetime), `date_to` (ISO 8601 datetime), `license` (string)

## Implementation Notes
- Follow the existing endpoint pattern in `modules/search/src/endpoints/mod.rs` and other endpoint files like `modules/fundamental/src/sbom/endpoints/list.rs` for query parameter extraction using Axum extractors
- Define a `SearchQuery` struct (or extend the existing one) with optional filter fields, deriving `Deserialize` for Axum's `Query` extractor
- Validate filter parameters:
  - `entity_type` must be one of "sbom", "advisory", "package" if provided
  - `severity` values should match known severity levels
  - `date_from` must be before or equal to `date_to` if both are provided
- Return `400 Bad Request` with a descriptive error message for invalid filter values using `AppError` from `common/src/error.rs`
- Per constraints doc section 5.2: inspect the existing endpoint implementation and Axum query parameter patterns before modifying
- The response format should remain `PaginatedResults<T>` — the filters narrow the result set but don't change the response structure

## Reuse Candidates
- `modules/search/src/endpoints/mod.rs` — Existing search endpoint handler to extend
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference for query parameter extraction pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` — Reference for list endpoint pattern
- `common/src/error.rs` — `AppError` for validation error responses

## Acceptance Criteria
- [ ] `GET /api/v2/search` accepts optional `entity_type` query parameter
- [ ] `GET /api/v2/search` accepts optional `severity` query parameter
- [ ] `GET /api/v2/search` accepts optional `date_from` and `date_to` query parameters
- [ ] `GET /api/v2/search` accepts optional `license` query parameter
- [ ] Invalid filter values return `400 Bad Request` with descriptive error messages
- [ ] Filters are passed through to `SearchService` correctly
- [ ] Existing search functionality (without filters) continues to work unchanged
- [ ] Response format remains `PaginatedResults<T>`

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `severity=critical` returns only critical advisories
- [ ] Integration test: search with date range returns only items within range
- [ ] Integration test: search with `license=MIT` returns only MIT-licensed packages
- [ ] Integration test: search with invalid `entity_type` returns 400
- [ ] Integration test: search with `date_from` after `date_to` returns 400
- [ ] Integration test: search without any filters returns results as before (backward compatibility)
- [ ] Integration test: search with multiple filters combined works correctly

## Dependencies
- Depends on: Task 4 — Upgrade SearchService to Use Full-Text Search with Relevance Ranking
