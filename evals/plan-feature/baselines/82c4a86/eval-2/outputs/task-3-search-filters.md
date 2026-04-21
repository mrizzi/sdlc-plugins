# Task 3 — Add filtering parameters to search endpoint

## Repository
trustify-backend

## Description
Add query-parameter-based filtering to the `GET /api/v2/search` endpoint. The
feature requires "some kind of filtering capability" but does not specify which
filters, which entities, or which fields.

**Ambiguity note:** This task cannot be fully specified because the feature does
not define:
- Which fields should be filterable (severity? date range? entity type? license?)
- Whether filters apply to the unified search endpoint, per-entity list endpoints,
  or both
- The expected API shape for filter parameters (e.g., `?type=advisory&severity=high`
  vs. a structured filter syntax)

This task assumes a minimal, safe starting point: add an entity-type filter
(`?type=sbom|advisory|package`) to the unified search endpoint, since that is the
most obvious filtering dimension given the existing multi-entity search. Additional
filters should be specified by the stakeholder before implementation.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add filter query parameters to the search endpoint handler
- `modules/search/src/service/mod.rs` — Extend `SearchService` to accept and apply filter criteria

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional `type` query parameter to filter results by entity type (sbom, advisory, package). Existing behavior without the parameter remains unchanged.

## Implementation Notes
- The existing query builder helpers in `common/src/db/query.rs` already support filtering and pagination patterns; use them to build the filter logic rather than implementing custom filtering from scratch
- Follow the pattern used by per-entity list endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs`) which already accept filter parameters; align the search endpoint's filter parameter naming and behavior with those existing endpoints
- Error handling must return `Result<T, AppError>` with `.context()` wrapping
- Response type must remain `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Ambiguity:** The entity-type filter is assumed as a minimum viable scope. The stakeholder may want field-level filters (e.g., `?severity=high`, `?date_from=2024-01-01`). Those would require additional work beyond this task and should be scoped as follow-up tasks once the specific filter requirements are clarified
- Per constraints doc section 5: changes must be scoped to the files listed; do not modify per-entity list endpoints in this task

## Reuse Candidates
- `common/src/db/query.rs` — Shared filtering and pagination helpers; reuse rather than implementing custom filter logic
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of an endpoint that already accepts filter query parameters; follow this pattern
- `modules/fundamental/src/advisory/endpoints/list.rs` — Another example of filtered list endpoint

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=package` returns only package results
- [ ] `GET /api/v2/search` without the `type` parameter returns all entity types (backward compatible)
- [ ] Invalid `type` values return a clear error response

## Test Requirements
- [ ] Integration test: search with `type=sbom` filter returns only SBOM results
- [ ] Integration test: search with `type=advisory` filter returns only advisory results
- [ ] Integration test: search without filter returns mixed results (backward compatibility)
- [ ] Integration test: search with invalid type filter returns error response
- [ ] Existing `tests/api/search.rs` tests pass without modification

## Verification Commands
- `cargo test --test search` — all search integration tests pass

## Documentation Updates
- `README.md` — Document the new `type` query parameter on the search endpoint
