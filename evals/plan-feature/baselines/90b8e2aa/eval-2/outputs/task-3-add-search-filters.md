## Repository
trustify-backend

## Target Branch
main

## Description
Add filter query parameters to the GET /api/v2/search endpoint so users can narrow search results by entity type, date range, and severity. The current search endpoint in `modules/search/src/endpoints/mod.rs` accepts only a query string with no filtering capability, forcing users to manually sift through all result types.

This task addresses the "add filters" requirement from TC-9002. **Assumption (pending clarification):** the feature description specifies "some kind of filtering capability" without defining which fields, operations, or filter combination logic. This task assumes the following filter parameters based on the existing data model:
- `entity_type` (enum: sbom, advisory, package) — filter by result type
- `date_from` / `date_to` (ISO 8601 date) — filter by creation or modification date range
- `severity` (enum matching AdvisorySummary severity field) — filter advisory results by severity level
- Multiple filters combine with AND semantics

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameter extraction and validation to the GET /api/v2/search handler
- `modules/search/src/service/mod.rs` — add filter application logic to the SearchService query builder

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type`, `date_from`, `date_to`, `severity`; response shape unchanged (PaginatedResults with existing fields)

## Implementation Notes
- Use the existing shared query builder helpers in `common/src/db/query.rs` for filter application. The module already provides filtering, pagination, and sorting utilities — extend or compose these for the search endpoint rather than writing new filter logic from scratch.
- Parse filter parameters using Axum query parameter extraction. Define a `SearchFilter` struct with optional fields for each filter parameter.
- Apply filters as WHERE clauses in the search query. When `entity_type` is specified, limit the search to that entity's table only. When date filters are specified, add date range conditions. When `severity` is specified, apply it only to advisory results.
- Error handling: return `AppError` with descriptive messages for invalid filter values (e.g., invalid date format, unknown entity type). Per project conventions, use `.context()` wrapping on all fallible operations. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust source file scope.
- Follow the endpoint registration pattern in `modules/search/src/endpoints/mod.rs` — the existing route registration structure should not change, only the handler's parameter extraction.
- The response type remains `PaginatedResults<T>` from `common/src/model/paginated.rs` — filters narrow the result set but do not change the response shape.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers with existing filtering support; primary reuse target for filter logic
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper, already used by the search endpoint
- `common/src/error.rs` — AppError enum for filter validation errors
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct containing the severity field definition (enum values to validate against)

## Acceptance Criteria
- [ ] GET /api/v2/search accepts optional `entity_type`, `date_from`, `date_to`, and `severity` query parameters
- [ ] When `entity_type` is provided, only results of that type are returned
- [ ] When `date_from` and/or `date_to` are provided, only results within the date range are returned
- [ ] When `severity` is provided, only advisory results matching that severity are returned
- [ ] Multiple filters combine with AND semantics (all specified filters must match)
- [ ] Invalid filter values return appropriate error responses (400 Bad Request with descriptive message)
- [ ] When no filters are provided, the endpoint behaves identically to its current behavior (backward compatible)

## Test Requirements
- [ ] Integration test: search with `entity_type=sbom` returns only SBOM results
- [ ] Integration test: search with `entity_type=advisory` returns only advisory results
- [ ] Integration test: search with date range filters returns only results within the range
- [ ] Integration test: search with `severity` filter returns only matching advisory results
- [ ] Integration test: search with multiple filters applies AND semantics
- [ ] Integration test: search with invalid filter values returns 400 error
- [ ] Integration test: search with no filters returns all results (backward compatibility)

## Verification Commands
- `cargo test -p tests --test search` — search integration tests pass
- `cargo test -p search` — module-level tests pass
