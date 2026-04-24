# Task 4 — Upgrade SearchService to Use Full-Text Search with Relevance Ranking

## Repository
trustify-backend

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to replace naive pattern matching with PostgreSQL full-text search using `tsvector`/`tsquery`. Add relevance ranking via `ts_rank` so that search results are ordered by relevance rather than arbitrarily. Integrate the filter predicates from Task 3 so that the service supports filtering by entity type, severity, date range, and license.

## Files to Modify
- `modules/search/src/service/mod.rs` — Replace existing search implementation with full-text search using `tsvector`/`tsquery`, add relevance ranking via `ts_rank`, integrate filter parameters

## Implementation Notes
- Inspect the current `SearchService` implementation in `modules/search/src/service/mod.rs` to understand the existing search logic before refactoring
- Use the full-text search query builder and filter predicate helpers added in Task 3 (`common/src/db/query.rs`)
- The search method should:
  1. Accept a search query string and optional filter parameters (entity_type, severity, date_range, license)
  2. Construct a `tsquery` from the search input using the helper from `common/src/db/query.rs`
  3. Match against the `search_vector` column on relevant entity tables
  4. Apply any active filters using the predicate builders
  5. Order results by `ts_rank(search_vector, tsquery)` descending for relevance
  6. Return results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs`
- Consider searching across multiple entity types (sbom, advisory, package) and unifying results — check how the current implementation handles this
- Use the entity definitions from `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` updated in Task 2
- Per constraints doc section 5.4: reuse the existing query helpers and pagination patterns rather than implementing parallel logic

## Reuse Candidates
- `common/src/db/query.rs` — Full-text search helpers and filter predicates (from Task 3)
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` search method as a reference for how services query entities
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` fetch/list methods as a reference pattern

## Acceptance Criteria
- [ ] `SearchService` uses PostgreSQL full-text search (`tsvector`/`tsquery`) instead of naive pattern matching
- [ ] Search results are ranked by relevance using `ts_rank`
- [ ] Filtering by entity type is supported (sbom, advisory, package)
- [ ] Filtering by severity is supported for advisory results
- [ ] Filtering by date range is supported
- [ ] Filtering by license is supported for package results
- [ ] Results are returned as `PaginatedResults<T>` with correct total counts
- [ ] Empty search queries return an appropriate response (e.g., empty results or recent items)

## Test Requirements
- [ ] Test that full-text search returns relevant results for known data
- [ ] Test that relevance ranking orders exact matches above partial matches
- [ ] Test filtering by entity type returns only the specified type
- [ ] Test filtering by severity returns only matching advisories
- [ ] Test filtering by date range returns only items within the range
- [ ] Test filtering by license returns only matching packages
- [ ] Test combined filters (e.g., entity_type + severity) work correctly
- [ ] Test empty/blank search query handling

## Dependencies
- Depends on: Task 2 — Update Entity Definitions for Full-Text Search Column
- Depends on: Task 3 — Extend Query Helpers with Full-Text Search and Filter Predicates
