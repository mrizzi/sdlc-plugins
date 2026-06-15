## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the search endpoint so users can narrow results by entity type and date range. The feature requirement "Add filters — Some kind of filtering capability" is deliberately vague. This task implements two filter dimensions as an MVP starting point: entity type filtering (SBOM, advisory, package) and date range filtering (created after/before).

**Assumptions pending clarification:**
- Filter dimensions are assumed to be: entity type (enum: `sbom`, `advisory`, `package`) and date range (`created_after`, `created_before`). The feature description specifies no filter fields, operators, or composition rules. This filter set needs product confirmation.
- Filters are assumed to be additive (AND composition): applying both entity type and date range filters returns only results matching both criteria. OR composition or nested filter expressions are not in scope.
- Filter parameters are passed as optional query parameters on the existing `GET /api/v2/search` endpoint. No new endpoints are required. This preserves backward compatibility — omitting filter parameters returns unfiltered results.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add filter parameters to the search service methods and apply them to the database query
- `modules/search/src/endpoints/mod.rs` — Parse filter query parameters from the HTTP request and pass them to the search service

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchFilter` struct containing optional entity type and date range filter fields

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `type` (enum: `sbom`, `advisory`, `package`), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date)

## Implementation Notes
- Define a `SearchFilter` struct in a new `modules/search/src/model/mod.rs` file, following the model pattern used by other modules (e.g., `modules/fundamental/src/sbom/model/mod.rs`).
- The `SearchFilter` struct should contain: `entity_type: Option<EntityType>` (an enum with variants `Sbom`, `Advisory`, `Package`), `created_after: Option<DateTime<Utc>>`, `created_before: Option<DateTime<Utc>>`.
- In `modules/search/src/endpoints/mod.rs`, deserialize filter parameters from query string using Axum's `Query<>` extractor pattern, consistent with how `modules/fundamental/src/sbom/endpoints/list.rs` handles query parameters.
- In `modules/search/src/service/mod.rs`, apply filters as additional WHERE clauses to the search query. Use the shared query builder helpers in `common/src/db/query.rs` for constructing filter conditions, following the filtering patterns already established there.
- When `entity_type` is provided, restrict the search to only the matching entity table(s). When date range filters are provided, add `created_at >= created_after` and/or `created_at <= created_before` conditions.
- All new handler code must return `Result<T, AppError>` per the error handling convention in `common/src/error.rs`.
- Invalid filter values (e.g., malformed date, unknown entity type) should return a 400 Bad Request with a descriptive error message.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers for filtering and pagination; the existing filtering pattern should be reused for the new filter parameters
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of query parameter parsing with Axum's `Query<>` extractor
- `modules/fundamental/src/sbom/model/mod.rs` — Example of model module structure to follow for the new search model

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?created_after=2024-01-01T00:00:00Z` returns only results created after the specified date
- [ ] `GET /api/v2/search?type=sbom&created_after=2024-01-01T00:00:00Z` correctly composes both filters (AND semantics)
- [ ] `GET /api/v2/search` without filter parameters returns all results (backward compatible)
- [ ] Invalid filter values return 400 Bad Request with a descriptive error message
- [ ] The response shape remains `PaginatedResults<T>` — no breaking changes to the API contract

## Test Requirements
- [ ] Integration test: filter by entity type returns only matching entity types
- [ ] Integration test: filter by date range returns only results within the specified range
- [ ] Integration test: combined filters (type + date range) apply AND semantics correctly
- [ ] Integration test: omitting all filters returns the same results as before (backward compatibility)
- [ ] Integration test: invalid entity type value returns 400 status
- [ ] Integration test: malformed date value returns 400 status

## Verification Commands
- `cargo test --test api search` — search-related integration tests pass

[sdlc-workflow] Description digest: sha256-md:9f43d7496e8d79d7a91c450c40063803024798446462aaf8048f4c8826afb9d6
