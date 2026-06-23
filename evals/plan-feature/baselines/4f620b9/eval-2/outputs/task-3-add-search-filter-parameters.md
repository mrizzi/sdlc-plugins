## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering parameters to the `GET /api/v2/search` endpoint to allow users to narrow search results by entity type, severity (for advisories), and date range. This addresses the "Add filters" requirement from TC-9002.

**Ambiguity note:** The feature does not specify which filters to add or how they should behave. This task assumes the following filter parameters based on the existing entity model:
- `entity_type` — filter by entity kind (sbom, advisory, package)
- `severity` — filter advisories by severity level (uses the `severity` field on `AdvisorySummary`)
- `created_after` / `created_before` — filter by creation date range

These assumptions should be validated with the product owner. Additional filters may be needed based on user feedback.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters to the search endpoint handler and route definition
- `modules/search/src/service/mod.rs` — extend SearchService to accept and apply filter criteria to search queries

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `entity_type` (string enum: sbom|advisory|package), `severity` (string), `created_after` (ISO 8601 date), `created_before` (ISO 8601 date)

## Implementation Notes
- Define a `SearchFilters` struct in `modules/search/src/service/mod.rs` or `modules/search/src/endpoints/mod.rs` to hold the filter parameters, using Axum's `Query` extractor for deserialization.
- Use the existing query builder helpers in `common/src/db/query.rs` for constructing WHERE clauses from filter parameters. This module already provides filtering, pagination, and sorting utilities — extend its patterns rather than creating new filter logic from scratch.
- For `entity_type` filtering: apply as a discriminator when searching across multiple entity tables (sbom, advisory, package).
- For `severity` filtering: apply as a WHERE clause on the advisory table's severity field (see `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`).
- For date range filtering: apply `created_after` and `created_before` as range conditions on the entity creation timestamp.
- All filter parameters must be optional — omitting a filter means no restriction on that dimension.
- Maintain backward compatibility: `GET /api/v2/search` with no filter params behaves identically to the current endpoint.
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3 (PR Rules): branch must be named after the Jira issue ID; after opening a PR, post its link as a comment on the Jira task.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse the filtering pattern for constructing WHERE clauses from the new filter parameters
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct contains the `severity` field that the severity filter will match against
- `modules/fundamental/src/sbom/endpoints/list.rs` — example of a list endpoint with query parameter extraction using Axum's `Query` extractor
- `modules/fundamental/src/advisory/endpoints/list.rs` — another list endpoint example demonstrating filter parameter patterns

## Acceptance Criteria
- [ ] `GET /api/v2/search?entity_type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?created_after=2024-01-01` returns only entities created after the specified date
- [ ] `GET /api/v2/search?created_before=2024-06-01` returns only entities created before the specified date
- [ ] Date range filters can be combined: `created_after` + `created_before`
- [ ] All filters are optional and can be combined with each other and with the search query
- [ ] Omitting all filters returns the same results as the current endpoint (backward compatibility)
- [ ] Invalid filter values return appropriate error responses

## Test Requirements
- [ ] Integration test: filter by entity_type returns only matching entity types
- [ ] Integration test: filter by severity returns only advisories with matching severity
- [ ] Integration test: filter by date range returns only entities within the range
- [ ] Integration test: combine multiple filters narrows results correctly
- [ ] Integration test: no filters returns all results (backward compatibility)
- [ ] Integration test: invalid filter values return 400 Bad Request

## Verification Commands
- `cargo test -p search` — search module compiles and unit tests pass
- `cargo test --test search` — search integration tests pass (in `tests/api/search.rs`)

## Documentation Updates
- `README.md` — document the new search filter query parameters (entity_type, severity, created_after, created_before) with usage examples

## Dependencies
- Depends on: Task 2 — Refactor SearchService for full-text search (filter logic builds on the refactored service)

[sdlc-workflow] Description digest: sha256-md:a9292d4488a500d1c70fdabcfa2c126c6822817342e1fa3b30092968a0ce9fce
