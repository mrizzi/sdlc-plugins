## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint to address TC-9002 requirement: "Add filters — some kind of filtering capability." This task introduces structured query parameters for filtering search results by entity type, severity, and date range, allowing users to narrow down search results to the most relevant subset.

**AMBIGUITY flagged**: The feature specifies "some kind of filtering capability" without defining which fields, operators, or UX patterns are needed. **ASSUMPTION pending clarification**: We implement server-side filters for: entity type (sbom/advisory/package), severity (for advisories: low/medium/high/critical), and date range (created_after/created_before). These are additive filters applied on top of the full-text search query. Additional filter fields can be added later based on product feedback.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Add query parameter structs for filter inputs (entity_type, severity, date_from, date_to). Validate and pass filters to the SearchService. Update route registration to document new parameters.
- `modules/search/src/service/mod.rs` — Extend the search method to accept a `SearchFilters` struct and apply WHERE clauses to the search query based on provided filters.
- `common/src/db/query.rs` — Add reusable filter builder functions for severity enum filtering and date range filtering that can be used by other list endpoints.

## Files to Create
- `modules/search/src/model/mod.rs` — Define `SearchFilters` struct (entity_type: Option<Vec<EntityType>>, severity: Option<Vec<Severity>>, date_from: Option<DateTime>, date_to: Option<DateTime>) and `SearchResult` response model with type discriminator.

## Implementation Notes
The filter implementation should integrate with the existing query helper patterns in `common/src/db/query.rs`. Follow the established patterns for filtering and pagination already present in that module.

For the endpoint in `modules/search/src/endpoints/mod.rs`:
1. Define a `SearchQuery` struct deriving `Deserialize` with optional filter fields
2. Parse `entity_type` as a comma-separated list: `?entity_type=sbom,advisory`
3. Parse `severity` as a comma-separated list: `?severity=high,critical`
4. Parse date range as ISO 8601: `?date_from=2024-01-01&date_to=2024-12-31`
5. Pass the parsed filters to `SearchService` alongside the existing search query

For the service in `modules/search/src/service/mod.rs`:
1. Apply entity type filter by conditionally including/excluding entity table queries from the UNION
2. Apply severity filter as a WHERE clause on the advisory sub-query
3. Apply date range filter as a WHERE clause on created_at/published_at columns

Per Key Conventions (Module pattern): Each domain module follows `model/ + service/ + endpoints/` structure. Applies: task creates `modules/search/src/model/mod.rs` matching the convention's module structure scope.

Per Key Conventions (Endpoint registration): Route registration in `modules/search/src/endpoints/mod.rs` must follow the established pattern. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

Per Key Conventions (Query helpers): Shared filtering logic belongs in `common/src/db/query.rs`. Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per Key Conventions (Error handling): All handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` and `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=term&entity_type=sbom` returns only SBOM results
- [ ] `GET /api/v2/search?q=term&severity=critical` returns only critical-severity advisories
- [ ] `GET /api/v2/search?q=term&date_from=2024-01-01&date_to=2024-06-30` returns only results within the date range
- [ ] Multiple filters can be combined: `?entity_type=advisory&severity=high&date_from=2024-01-01`
- [ ] Invalid filter values return 400 Bad Request with descriptive error messages
- [ ] Omitting all filters returns unfiltered results (backward compatible)
- [ ] Filtered results are still ranked by relevance (or user-specified sort)

## Test Requirements
- [ ] Filter by single entity type returns only that type
- [ ] Filter by multiple entity types returns matching types
- [ ] Severity filter applies only to advisory results and correctly narrows results
- [ ] Date range filter correctly bounds results by creation/publish date
- [ ] Combined filters intersect correctly (AND semantics)
- [ ] Invalid severity value returns 400
- [ ] Invalid date format returns 400
- [ ] No filters returns same results as unfiltered search

## Dependencies
- Depends on: Task 2 — Search relevance ranking (filters operate on top of the full-text search and ranking infrastructure)

## API Changes
- `GET /api/v2/search` adds optional query parameters:
  - `entity_type` — comma-separated list: `sbom`, `advisory`, `package`
  - `severity` — comma-separated list: `low`, `medium`, `high`, `critical`
  - `date_from` — ISO 8601 date, inclusive lower bound
  - `date_to` — ISO 8601 date, inclusive upper bound

[sdlc-workflow] Description digest: sha256-md:977948257be0122e2fe146a983539e84554d1cc04f19ea1b827e18719cddaa84
