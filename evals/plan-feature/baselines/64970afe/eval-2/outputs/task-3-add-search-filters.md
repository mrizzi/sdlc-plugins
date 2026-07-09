## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capabilities to the search endpoint, allowing users to narrow search results by specific criteria. This addresses user feedback that search returns too many irrelevant results by enabling targeted filtering alongside the full-text search.

**Ambiguity notice:** The feature description specifies "add filters -- some kind of filtering capability" without defining which filter dimensions are needed. This task assumes an initial set of filters: entity type, date range, and severity (assumption A4 -- pending clarification from product owner). Filters use AND semantics when combined (assumption A5 -- pending clarification). The specific filter values and valid ranges should be confirmed before implementation.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` -- Add filter query parameters (entity_type, date_from, date_to, severity) to the search endpoint
- `modules/search/src/service/mod.rs` -- Implement filter logic in SearchService to compose filter predicates with the search query
- `common/src/db/query.rs` -- Extend query builder helpers with filter combinator functions for search-specific filters

## API Changes
- `GET /api/v2/search` -- MODIFY: Add optional query parameters `entity_type` (string enum: sbom|advisory|package), `date_from` (ISO 8601 date), `date_to` (ISO 8601 date), `severity` (string enum matching advisory severity levels)

## Implementation Notes
- Add the following optional query parameters to `GET /api/v2/search`:
  - `entity_type` -- filter by entity type (sbom, advisory, package)
  - `date_from` / `date_to` -- filter by date range (ISO 8601 format)
  - `severity` -- filter by severity level (applicable to advisories; see severity field in `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary`)
- Use the existing query builder pattern in `common/src/db/query.rs` for composing filter predicates; extend with new filter combinator functions
- Filters should compose with AND semantics -- multiple active filters narrow the result set
- All filter parameters must be optional -- omitting a filter means no restriction on that dimension
- Follow the existing endpoint parameter parsing pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for adding query parameters to the Axum handler
- Ensure filtered results still return `PaginatedResults<T>` and work correctly with relevance ranking from Task 2
- Use SeaORM `Condition::all()` for composing multiple filter predicates
- Invalid filter values (e.g., invalid date format, unknown entity type) should return appropriate error responses using the `AppError` enum from `common/src/error.rs`

Per CONVENTIONS.md §Error Handling: all new or modified handler methods must return `Result<T, AppError>` with `.context()` wrapping for invalid filter parameter errors. See `common/src/error.rs` for the AppError enum.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query Helpers: extend shared filtering utilities in `common/src/db/query.rs` for search-specific filters rather than implementing ad-hoc filter logic in the service layer.
Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

Per CONVENTIONS.md §Response Types: filtered search results must continue to return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.

Per CONVENTIONS.md §Endpoint Registration: the search endpoint route registration in `modules/search/src/endpoints/mod.rs` must remain consistent with the route mounting pattern in `server/src/main.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint registration scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Existing filtering and pagination utilities to extend with search-specific filter combinators
- `modules/fundamental/src/sbom/endpoints/list.rs` -- Reference implementation for Axum endpoint query parameter parsing pattern
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Reference for severity field structure used in severity filter logic
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` -- Reference for entity type structures including license field

## Acceptance Criteria
- [ ] Search endpoint accepts optional filter parameters: entity_type, date_from, date_to, severity
- [ ] Each filter narrows the search results to matching entries only
- [ ] Multiple filters combine with AND semantics
- [ ] Omitting a filter parameter returns unfiltered results for that dimension
- [ ] Invalid filter values return appropriate error responses (400 Bad Request)
- [ ] Filtered results maintain correct pagination and relevance ranking
- [ ] Existing API consumers are unaffected (all new parameters are optional -- backward compatible)

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying entity_type filter returns only matching entity types
- [ ] Integration test verifying date range filter narrows results to the specified time window
- [ ] Integration test verifying severity filter applies correctly to advisory results
- [ ] Integration test verifying multiple filters combine with AND semantics
- [ ] Integration test verifying omitted filters return unfiltered results
- [ ] Integration test verifying invalid filter values return 400 error responses

## Verification Commands
- `cargo test --test search` -- Verify search integration tests pass
- `cargo build` -- Verify project compiles without errors

## Dependencies
- Depends on: Task 1 -- Optimize search query performance (filter logic builds on the optimized query infrastructure)
- Depends on: Task 2 -- Improve search result relevance ranking (filters must compose correctly with relevance ranking)
