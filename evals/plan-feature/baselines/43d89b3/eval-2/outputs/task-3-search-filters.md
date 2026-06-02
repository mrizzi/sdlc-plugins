## Repository
trustify-backend

## Target Branch
main

## Description
Add filter parameters to the search endpoint to allow users to narrow search results by entity type, severity, and date range. The feature description specifies "some kind of filtering capability" without detailing which filters are needed.

**Ambiguity note:** The feature description does not specify which fields should be filterable, what filter types are needed (dropdown, range, text, date), or whether filters apply to the unified search endpoint or individual entity list endpoints. **Assumption pending clarification:** We assume filters should be added to the unified search endpoint (`GET /api/v2/search`) with the following filter parameters: `entity_type` (enum: sbom, advisory, package), `severity` (for advisories), `date_from` and `date_to` (ISO 8601 date range for creation date). The product owner should confirm the filter set and whether additional filters are required.

## Files to Modify
- `modules/search/src/service/mod.rs` — extend `SearchService` to accept and apply filter parameters in queries
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the `GET /api/v2/search` endpoint

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (enum: sbom|advisory|package), `severity` (string), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date)

## Implementation Notes
Extend the `GET /api/v2/search` endpoint in `modules/search/src/endpoints/mod.rs` to accept optional filter query parameters. These are additive (non-breaking) changes to the existing endpoint.

Implement filtering logic in `SearchService` (`modules/search/src/service/mod.rs`):
1. `entity_type` filter: restrict results to a specific entity type (sbom, advisory, or package). Use the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to build type-specific queries.
2. `severity` filter: when searching advisories, filter by severity field from `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs`).
3. `date_from` / `date_to` filters: filter results by creation date range.

Use the shared filtering helpers in `common/src/db/query.rs` — this module already provides filtering and pagination infrastructure. Extend the existing filter builder pattern rather than creating new filtering code.

All filter parameters should be optional. When no filters are provided, behavior is identical to current search (all entity types, no date restriction).

Response format remains `PaginatedResults<T>` from `common/src/model/paginated.rs`.

Error handling: validate filter parameter values and return appropriate `AppError` responses (from `common/src/error.rs`) for invalid inputs (e.g., invalid date format, unknown entity type).

Per docs/constraints.md:
- §2 (Commit Rules): commits must reference TC-9002, follow Conventional Commits, and include the Assisted-by trailer.
- §3 (PR Rules): branch must be named after the Jira issue ID; PR link must be posted to the task.
- §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder with existing filtering and pagination helpers; extend for new filter types
- `common/src/model/paginated.rs::PaginatedResults<T>` — existing response wrapper
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — has severity field to use for severity filtering
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing advisory search/list logic that may inform filter implementation patterns
- `common/src/error.rs::AppError` — error handling pattern for input validation

## Acceptance Criteria
- [ ] `GET /api/v2/search` accepts optional `entity_type` parameter to filter by sbom, advisory, or package
- [ ] `GET /api/v2/search` accepts optional `severity` parameter to filter advisories by severity
- [ ] `GET /api/v2/search` accepts optional `date_from` and `date_to` parameters for date range filtering
- [ ] All filter parameters are optional; omitting them returns unfiltered results (existing behavior)
- [ ] Multiple filters can be combined (e.g., entity_type=advisory AND severity=high)
- [ ] Invalid filter values return appropriate error responses
- [ ] Response format remains `PaginatedResults<T>`

## Test Requirements
- [ ] Integration test verifying `entity_type=sbom` returns only SBOM results
- [ ] Integration test verifying `entity_type=advisory` returns only advisory results
- [ ] Integration test verifying `entity_type=package` returns only package results
- [ ] Integration test verifying `severity` filter returns only advisories with matching severity
- [ ] Integration test verifying `date_from` and `date_to` filter restricts results to the specified date range
- [ ] Integration test verifying combined filters work correctly (e.g., entity_type + severity)
- [ ] Integration test verifying omitted filters return all results (backward compatibility)
- [ ] Integration test verifying invalid filter values return error responses
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — all search tests pass including new filter tests

## Documentation Updates
- `README.md` — document new search filter query parameters and usage examples
