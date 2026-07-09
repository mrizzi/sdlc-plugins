## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results in the SearchService. Currently, search results are returned without meaningful relevance ordering, leading to user complaints about irrelevant results. This task adds scoring and ranking logic so that results most relevant to the search query appear first.

**Ambiguity notice:** The feature description specifies "results should be more relevant" without defining relevance criteria. This task assumes relevance ranking uses PostgreSQL full-text search scoring (ts_rank) with higher weight for exact matches over partial matches (assumption A2 -- pending clarification from product owner). The search scope is assumed to cover all entity types: SBOMs, advisories, and packages (assumption A3 -- pending clarification).

## Files to Modify
- `modules/search/src/service/mod.rs` -- Implement relevance scoring using PostgreSQL ts_rank and order results by relevance score
- `modules/search/src/endpoints/mod.rs` -- Update the search endpoint to support an optional sort parameter (relevance, alphabetical, date)
- `modules/search/src/lib.rs` -- Export the new model module

## Files to Create
- `modules/search/src/model/mod.rs` -- Search result model with relevance score field for ranked results

## Implementation Notes
- Use PostgreSQL `ts_rank()` or `ts_rank_cd()` functions to compute relevance scores against `tsvector` columns (created by Task 1's migration)
- Define a `SearchResult` struct in the new model module that wraps entity summaries with a relevance score field
- Follow the existing module pattern: the new `model/` directory in the search module mirrors the structure in `modules/fundamental/src/sbom/model/` and `modules/fundamental/src/advisory/model/`
- Update `modules/search/src/lib.rs` to export the new model module
- The search endpoint should default to relevance-based ordering when a search query is provided
- Weight exact matches higher than partial matches in the ranking function
- Ensure the endpoint continues to return `PaginatedResults<T>` as per the existing response type convention, using `common/src/model/paginated.rs`

Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the search module. See `modules/fundamental/src/sbom/` for reference.
Applies: task creates `modules/search/src/model/mod.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Error Handling: all new or modified handler and service methods must return `Result<T, AppError>` with `.context()` wrapping. See `common/src/error.rs` for the AppError enum.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Response Types: list and search endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint file scope.

## Reuse Candidates
- `common/src/model/paginated.rs::PaginatedResults<T>` -- Existing pagination wrapper to use for ranked search results
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` -- Reference model struct pattern for the new SearchResult model
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Additional reference for model struct conventions including severity field

## Acceptance Criteria
- [ ] Search results are ranked by relevance score when a text query is provided
- [ ] Exact matches rank higher than partial matches in search results
- [ ] A SearchResult model exists with a relevance score field
- [ ] An optional sort parameter allows switching between relevance, alphabetical, and date ordering
- [ ] Default sort order is by relevance when a search query is present
- [ ] Existing search API response shape (PaginatedResults) is preserved

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying results are ordered by relevance (exact match appears before partial match)
- [ ] Integration test verifying the sort parameter changes result ordering
- [ ] Integration test verifying default behavior returns relevance-ranked results when a query term is provided

## Verification Commands
- `cargo test --test search` -- Verify search integration tests pass
- `cargo build` -- Verify project compiles without errors

## Dependencies
- Depends on: Task 1 -- Optimize search query performance (requires the GIN indexes and tsvector columns for ts_rank scoring)
