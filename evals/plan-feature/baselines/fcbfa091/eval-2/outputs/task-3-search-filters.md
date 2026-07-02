additional_fields: { "labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": ["RHTPA 1.6.0"] }

## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow search results by entity type, date range, and severity. The feature description says "Add filters -- Some kind of filtering capability" without specifying which filters, filter UX, or filter combinations.

**Assumption (pending clarification):** "Some kind of filtering capability" is interpreted as server-side query parameter filters on the `GET /api/v2/search` endpoint. The following filters are assumed based on the existing entity model:
- `type` -- filter by entity type (sbom, advisory, package)
- `date_from` / `date_to` -- filter by creation or modification date range
- `severity` -- filter advisories by severity level (uses the severity field on AdvisorySummary)

These filters are additive (AND semantics). Additional filters would require product clarification.

**Ambiguity:** The feature does not specify which attributes should be filterable, whether filters should support multi-select or single-select, whether filters combine with AND or OR semantics, or how filters interact with relevance ranking. This task implements the most commonly useful filters based on the existing data model. Further filter requirements need product owner input.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add query parameter parsing for `type`, `date_from`, `date_to`, and `severity` filter parameters on the `GET /api/v2/search` endpoint
- `modules/search/src/service/mod.rs` -- Extend SearchService to accept filter parameters and apply them as WHERE clauses in the search query

## API Changes
- `GET /api/v2/search` -- MODIFY: Add optional query parameters `type` (string enum: sbom|advisory|package), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date), `severity` (string enum matching advisory severity levels). All filters are optional; when provided, they narrow the result set with AND semantics.

## Implementation Notes
- Follow the existing filtering patterns established in the list endpoints. Reference `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for how query parameters are parsed and passed to service methods.
- Use the shared query builder helpers in `common/src/db/query.rs` for constructing filter WHERE clauses. The existing filtering infrastructure handles pagination and sorting; extend it with the new filter predicates.
- For the `type` filter, the SearchService needs to conditionally join or query only the relevant entity tables (sbom, advisory, package). Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`.
- For the `severity` filter, reference the `severity` field on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`. When severity is provided but the type filter is not "advisory", the severity filter should be silently ignored (not error).
- For date range filters, use the timestamp columns on the entities. Apply >= for `date_from` and <= for `date_to`.
- All handlers must return `Result<T, AppError>` with `.context()` wrapping for error cases (e.g., invalid date format, unknown type value).
- Results must continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Per CONVENTIONS.md: use the shared query builder helpers from `common/src/db/query.rs` for filter construction, following the same patterns used by existing list endpoints.
  Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Shared query builder with existing filtering and pagination helpers; extend with new filter predicates
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Reference for query parameter parsing pattern in list endpoints
- `modules/fundamental/src/advisory/endpoints/list.rs` -- Reference for query parameter parsing pattern including advisory-specific fields
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Contains the severity field definition used for severity filtering
- `common/src/model/paginated.rs::PaginatedResults` -- Response wrapper; continue using for filtered search results

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=package` returns only package results
- [ ] `GET /api/v2/search?date_from=2024-01-01&date_to=2024-12-31` returns only results within the date range
- [ ] `GET /api/v2/search?severity=critical` returns only advisories with critical severity
- [ ] Multiple filters combine with AND semantics (e.g., `type=advisory&severity=high` returns only high-severity advisories)
- [ ] Filters work correctly in combination with search query terms and relevance ranking
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Omitting all filters returns unfiltered results (backward compatible)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying each filter parameter independently
- [ ] Integration test verifying combined filters (type + severity, type + date range)
- [ ] Integration test verifying invalid filter values return 400 status
- [ ] Integration test verifying backward compatibility (no filters = same behavior as before)

## Dependencies
- Depends on: Task 1 -- Add database indexes for search performance optimization (requires the optimized search query infrastructure)
