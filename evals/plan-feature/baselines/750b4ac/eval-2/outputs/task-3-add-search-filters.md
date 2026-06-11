# Task 3 — Add filter parameters to the search endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the `GET /api/v2/search` endpoint by supporting query parameters for entity type, severity, and date range. This addresses the "add filters" MVP requirement from TC-9002. Filters are applied as additional WHERE clauses combined with the full-text search query, narrowing results before ranking.

**Assumption pending clarification:** The feature specifies "some kind of filtering capability" without defining which fields are filterable. We assume the following filters based on existing entity model attributes: `entity_type` (enum: sbom, advisory, package), `severity` (for advisories, based on the severity field in `AdvisorySummary`), and `date_from`/`date_to` (date range filter). Additional filters can be added incrementally in follow-up work.

**Assumption pending clarification:** Filter combination semantics are assumed to be AND (all filters must match). No OR-based or complex filter expression language is planned. This should be confirmed with the team.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — add filter query parameters (`entity_type`, `severity`, `date_from`, `date_to`) to the `GET /api/v2/search` handler; pass filters to the SearchService
- `modules/search/src/service/mod.rs` — accept filter parameters in the search method; apply them as WHERE clauses in the search query alongside full-text search
- `common/src/db/query.rs` — add or extend shared filtering helpers to support the new filter types (enum match, date range)

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters: `entity_type` (string enum: "sbom", "advisory", "package"), `severity` (string, applicable to advisories), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date). All filters are optional and combined with AND semantics.

## Implementation Notes
- Inspect the existing query helpers in `common/src/db/query.rs` — filtering, pagination, and sorting helpers already exist. Extend these rather than creating new filter infrastructure.
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field — use this as the basis for the severity filter.
- Follow the existing list endpoint patterns in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` — these demonstrate how query parameters are parsed and passed to service methods.
- Endpoint registration follows the pattern in `modules/search/src/endpoints/mod.rs` — the route is already registered at `/api/v2/search`.
- All handlers return `Result<T, AppError>` with `.context()` wrapping — maintain this pattern for filter validation errors (e.g., invalid date format, unknown entity type).
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response — filters should not change the response wrapper.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits and reference TC-9002 in the footer.
- Per docs/constraints.md §5 (Code Change Rules): reuse existing filtering helpers in `common/src/db/query.rs`; do not create duplicate filter logic.

## Reuse Candidates
- `common/src/db/query.rs` — existing shared filtering, pagination, and sorting helpers; extend for the new filter types
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates query parameter parsing and service method invocation pattern for list endpoints
- `modules/fundamental/src/advisory/endpoints/list.rs` — demonstrates query parameter parsing for advisory-specific filters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — contains the severity field used for severity filtering

## Acceptance Criteria
- [ ] The `GET /api/v2/search` endpoint accepts optional `entity_type`, `severity`, `date_from`, and `date_to` query parameters
- [ ] Filters narrow search results correctly when provided (AND semantics)
- [ ] Omitting all filters returns unfiltered search results (backward compatible)
- [ ] Invalid filter values (unknown entity type, malformed date) return appropriate error responses
- [ ] Severity filter applies only when searching advisories or when entity_type is "advisory"
- [ ] Filters combine correctly with full-text search and relevance ranking

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: verify filtering by entity_type returns only results of that type
- [ ] Integration test: verify filtering by severity returns only matching advisories
- [ ] Integration test: verify date range filtering returns only results within the specified range
- [ ] Integration test: verify combining multiple filters (entity_type + severity) works correctly
- [ ] Integration test: verify that omitting filters returns all results (backward compatibility)
- [ ] Integration test: verify invalid filter values return appropriate error responses

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search API integration tests pass

## Dependencies
- Depends on: Task 2 — Refactor SearchService to use PostgreSQL full-text search with relevance ranking

[sdlc-workflow] Description digest: sha256-md:1c0ade13fe4d6e9d774655af40487572a9eaa214b8add5abefd98a44f738a2ef
