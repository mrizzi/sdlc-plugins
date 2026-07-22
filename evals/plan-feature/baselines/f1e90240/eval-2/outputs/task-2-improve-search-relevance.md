## Repository

trustify-backend

## Target Branch

main

## Description

Improve the relevance of search results returned by the `SearchService` so that users receive more useful results when querying the `GET /api/v2/search` endpoint. Users have reported that search returns "irrelevant results," but no specific examples or ranking criteria have been provided.

This task introduces result ranking/scoring to the search service, so that results matching more search terms or matching in higher-priority fields (e.g., name/title fields vs. description fields) are ranked higher in the response.

**Assumptions (pending clarification):**
- **AMBIGUITY: No definition of "relevant" or ranking criteria.** The feature states results should be "more relevant" but does not define what constitutes relevance. This task assumes relevance means: (1) exact matches ranked above partial matches, (2) matches in name/title fields ranked above matches in description/body fields, (3) results ordered by a computed relevance score. These assumptions need stakeholder validation.
- **AMBIGUITY: Entity type priority is unspecified.** The search endpoint searches across multiple entity types (SBOMs, advisories, packages). The feature does not specify whether certain entity types should be prioritized in results. This task assumes equal weighting across entity types, pending clarification.

## Acceptance Criteria

- [ ] Search results are ordered by a relevance score rather than default database ordering
- [ ] Exact matches in name/title fields are ranked higher than partial matches
- [ ] Matches in name/title fields are ranked higher than matches in description/body fields
- [ ] The relevance scoring logic is encapsulated in the search service, not scattered across entity modules
- [ ] Existing search queries continue to return the same result sets (ordering may change, but no results are lost)
- [ ] The search response includes a relevance score field for each result (enabling future UI display)

## Files to Modify

- `modules/search/src/service/mod.rs` -- Add relevance scoring and result ranking logic to `SearchService`
- `modules/search/src/endpoints/mod.rs` -- Update the `GET /api/v2/search` endpoint to pass ranking parameters and return scored results

## Implementation Notes

- Modify `SearchService` in `modules/search/src/service/mod.rs` to compute relevance scores for search results. If PostgreSQL full-text search is used (as introduced by Task 1), leverage `ts_rank` or `ts_rank_cd` functions for relevance scoring.
- The search endpoint in `modules/search/src/endpoints/mod.rs` registers routes at `/api/v2/search`. Update the handler to accept an optional sort-by-relevance parameter and default to relevance-based ordering.
- Follow the existing module pattern (`model/ + service/ + endpoints/`) when adding any new model structs for scored results.
- Entity models such as `SbomSummary` in `modules/fundamental/src/sbom/model/summary.rs`, `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`, and `PackageSummary` in `modules/fundamental/src/package/model/summary.rs` define the fields available for weighted ranking (name, title, description).
- All handlers must return `Result<T, AppError>` with `.context()` wrapping per the error handling convention.

**Convention: Module pattern** -- Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's module scope. Each domain module follows `model/ + service/ + endpoints/` structure.

**Convention: Error handling** -- Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's Rust service/endpoint scope. All handlers return `Result<T, AppError>` with `.context()` wrapping.

## Dependencies

- Task 1 (Optimize search performance) -- relevance scoring builds on the full-text search indexes introduced in Task 1

## Test Requirements

- Add integration tests in `tests/api/search.rs` verifying that exact matches are ranked higher than partial matches
- Add tests verifying that name/title field matches are ranked higher than description field matches
- Add tests verifying that the relevance score is included in the search response
- Add tests verifying that result sets are complete (no results lost due to ranking changes)
- Follow the existing integration test pattern using real PostgreSQL test database with `assert_eq!(resp.status(), StatusCode::OK)` pattern
