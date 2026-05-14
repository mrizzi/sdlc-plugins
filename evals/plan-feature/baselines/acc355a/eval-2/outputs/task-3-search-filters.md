# Task 3 — Add search filter support

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow search results by entity type and advisory severity. The filters are applied as query parameters on the existing `GET /api/v2/search` endpoint.

**Ambiguity note:** The feature description says "Add filters — some kind of filtering capability" without specifying which filters. This task implements two filters based on the existing data model: entity type (sbom, advisory, package) and severity (for advisories, based on the `severity` field in `AdvisorySummary`). Additional filters (e.g., date range, license type, ingestion source) should be specified in follow-up requirements if needed.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add filter parameters to the search query logic: filter by entity type and by advisory severity
- `modules/search/src/endpoints/mod.rs` — Accept `entity_type` and `severity` query parameters on `GET /api/v2/search` and pass them to the service layer

## API Changes
- `GET /api/v2/search` — MODIFY: Add optional query parameters `entity_type` (enum: `sbom`, `advisory`, `package`) and `severity` (string, e.g., `critical`, `high`, `medium`, `low`). When provided, results are filtered to match the specified criteria. Both filters are optional and can be combined.

## Implementation Notes
- Use the existing query builder helpers in `common/src/db/query.rs` for constructing filter predicates. The shared filtering infrastructure already supports adding WHERE clauses — compose with it rather than building custom filter logic.
- The `entity_type` filter should restrict which entity tables are queried during search. When `entity_type=advisory`, only query the advisory table; when omitted, query all entity types.
- The `severity` filter applies only to advisory results. Use the `severity` field from the advisory entity (`entity/src/advisory.rs`) and the `AdvisorySummary` model (`modules/fundamental/src/advisory/model/summary.rs`). When `severity` is specified but `entity_type` is not, it should implicitly filter to advisory results only.
- Follow the existing endpoint parameter pattern in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for how query parameters are parsed and validated in Axum handlers.
- Maintain backward compatibility: requests without filter parameters should return the same results as before (all entity types, no severity filter).
- Return results using `PaginatedResults<T>` from `common/src/model/paginated.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — Shared query builder helpers with existing filtering infrastructure to compose with
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct containing the `severity` field used for filtering
- `modules/fundamental/src/sbom/endpoints/list.rs` — Example of how list endpoints parse query parameters in Axum
- `modules/fundamental/src/advisory/endpoints/list.rs` — Example of advisory list endpoint with parameter handling

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?entity_type=package` returns only package results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?entity_type=advisory&severity=high` correctly combines both filters
- [ ] `GET /api/v2/search` without filter parameters returns results from all entity types (backward compatible)
- [ ] Invalid filter values return an appropriate error response

## Test Requirements
- [ ] Integration test verifying entity_type filter returns only the specified type
- [ ] Integration test verifying severity filter returns only advisories matching the severity level
- [ ] Integration test verifying combined filters (entity_type + severity) work correctly
- [ ] Integration test verifying that omitting filters returns all entity types (backward compatibility)
- [ ] Integration test verifying that invalid filter values return an error response

## Dependencies
- Depends on: Task 2 — Implement ranked full-text search in SearchService
