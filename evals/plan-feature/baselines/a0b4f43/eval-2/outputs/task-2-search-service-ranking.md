## Repository
trustify-backend

## Target Branch
main

## Description
Extend the SearchService to use PostgreSQL full-text search with weighted ranking instead of basic text matching. This addresses the TC-9002 requirement that "results should be more relevant" by implementing `ts_rank` scoring so that exact matches and title matches are ranked higher than partial or description-only matches. The service should search across all three entity types (SBOMs, advisories, packages) and return results ordered by relevance score.

**Assumption (pending clarification):** Relevance is defined as weighted full-text match scoring. The product owner should confirm whether certain entity types should be prioritized over others in mixed results, and whether any domain-specific ranking factors apply beyond text matching.

## Files to Modify
- `modules/search/src/service/mod.rs` — Refactor SearchService to use `tsvector`-based full-text search with `ts_rank` scoring, replacing any existing LIKE/ILIKE queries
- `modules/search/src/lib.rs` — Update module exports if new types are introduced

## Files to Create
- `modules/search/src/model/mod.rs` — Search result model with relevance score, entity type discriminator, and unified result shape

## Implementation Notes
- Use PostgreSQL `ts_query` and `ts_rank` functions to perform ranked full-text search against the `search_vector` columns added in Task 1.
- Implement weighted ranking: use `ts_rank(search_vector, query, 1)` with the weight configuration set during indexing (title = 'A', description = 'B').
- The SearchService should query all three entity tables (sbom, advisory, package), compute a relevance score for each match, and return a unified result set sorted by descending score.
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` (SbomService) for method structure and error handling.
- All service methods must return `Result<T, AppError>` with `.context()` wrapping, consistent with the error handling pattern in `common/src/error.rs`.
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response shape to maintain consistency with other list endpoints.
- Reuse query builder helpers from `common/src/db/query.rs` for pagination and sorting.
- Per docs/constraints.md §5.4: Reuse existing utilities — leverage `common/src/db/query.rs` for pagination rather than writing custom pagination logic.
- Per docs/constraints.md §2.1-2.3: Commits must reference TC-9002, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs` — SbomService pattern for service method structure, error handling, and database query patterns
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService including its existing `search` method that may contain reusable search logic
- `common/src/db/query.rs` — Shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` — PaginatedResults<T> wrapper for list responses
- `common/src/error.rs` — AppError enum for consistent error handling

## Acceptance Criteria
- [ ] SearchService uses full-text search with `tsvector` and `ts_rank` instead of basic text matching
- [ ] Search results include a relevance score and are sorted by descending relevance
- [ ] Search spans all three entity types: SBOMs, advisories, and packages
- [ ] Results are returned in the `PaginatedResults<T>` format
- [ ] Exact title matches rank higher than partial description matches
- [ ] Empty search queries return an appropriate response (empty results or validation error)

## Test Requirements
- [ ] Test that a search query matching a title exactly ranks that result highest
- [ ] Test that search spans all entity types and returns mixed results
- [ ] Test that pagination works correctly with search results
- [ ] Test that an empty or whitespace-only query is handled gracefully
- [ ] Test that special characters in search queries do not cause errors

## Dependencies
- Depends on: Task 1 — Search index migration (requires tsvector columns and GIN indexes to be in place)
