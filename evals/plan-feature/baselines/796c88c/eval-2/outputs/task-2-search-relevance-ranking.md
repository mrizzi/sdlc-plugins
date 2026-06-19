# Task 2: Full-Text Search Service with Relevance Ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` to use PostgreSQL full-text search with relevance ranking instead of basic text matching. This task addresses two requirements from TC-9002: "search should be faster" (by using GIN-indexed queries) and "results should be more relevant" (by scoring results with `ts_rank`).

**Ambiguity: "Results should be more relevant"** — The feature does not define what "relevant" means. It could mean: (a) results matching the query terms should rank higher, (b) exact matches should appear before partial matches, (c) certain entity types should be prioritized, or (d) recent items should rank higher. This implementation assumes relevance means PostgreSQL ts_rank scoring with default weights, which ranks results by term frequency and proximity. If the product owner has specific relevance criteria (e.g., boosting advisories with critical severity, or recency weighting), the ranking logic will need adjustment.

**Assumption (A3)**: Relevance ranking uses PostgreSQL `ts_rank` with default D-weight configuration `{0.1, 0.2, 0.4, 1.0}`. Custom weighting per field (e.g., title matches ranked higher than description matches) would require `setweight()` in the tsvector generation, which would need a migration change in Task 1.

## Files to Modify
- `modules/search/src/service/mod.rs` — Replace existing search query logic with full-text search using `to_tsquery()` and `ts_rank()` scoring; return results ordered by relevance score
- `common/src/db/query.rs` — Add a shared full-text search query builder helper that constructs `WHERE search_vector @@ to_tsquery($1) ORDER BY ts_rank(search_vector, to_tsquery($1)) DESC` clauses, consistent with the existing filtering/pagination/sorting helpers
- `common/src/model/paginated.rs` — Potentially extend `PaginatedResults<T>` to include an optional relevance score field, or keep scores internal to ranking only

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Refactor it to:
  1. Parse the user query into a tsquery using `plainto_tsquery('english', $1)` for natural language input or `to_tsquery('english', $1)` for advanced syntax
  2. Execute `WHERE search_vector @@ tsquery` against each entity table (sbom, advisory, package)
  3. Score results with `ts_rank(search_vector, tsquery)` and order by score descending
  4. Merge results across entity types, maintaining score-based ordering
- Follow the error handling pattern: all service methods return `Result<T, AppError>` with `.context()` wrapping, consistent with patterns in `modules/fundamental/src/sbom/service/sbom.rs` and `modules/fundamental/src/advisory/service/advisory.rs`
- Use the query builder helpers from `common/src/db/query.rs` for pagination — the existing pattern supports `PaginatedResults<T>` from `common/src/model/paginated.rs`
- The search endpoint at `modules/search/src/endpoints/mod.rs` (GET /api/v2/search) should continue to work with the same API contract but now returns relevance-ranked results
- Consider adding `ts_headline()` to generate search result snippets with highlighted matches — this improves perceived relevance for API consumers

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`@@ to_tsquery`) instead of LIKE/ILIKE
- [ ] Search results are ordered by relevance score (ts_rank) in descending order
- [ ] Search works across all three entity types: SBOMs, advisories, and packages
- [ ] Multi-word queries return results matching all terms (AND semantics via plainto_tsquery)
- [ ] Empty or whitespace-only queries return an appropriate error or empty result set
- [ ] The GET /api/v2/search endpoint continues to return `PaginatedResults<T>`
- [ ] Query helper in `common/src/db/query.rs` is reusable by other modules

## Test Requirements
- [ ] Integration test: search for a known SBOM name returns the correct SBOM as the top result
- [ ] Integration test: search for an advisory title returns the matching advisory ranked first
- [ ] Integration test: multi-word query returns results containing all terms
- [ ] Integration test: search query matching multiple entity types returns results from all types, ordered by relevance
- [ ] Integration test: search for a non-existent term returns empty results with 200 status
- [ ] Integration test: empty query string returns 400 Bad Request or empty results (decide on behavior)
- [ ] Tests in `tests/api/search.rs` following the existing `assert_eq!(resp.status(), StatusCode::OK)` pattern

## Dependencies
- Depends on: Task 1 — Database Migration for Full-Text Search Indexes (tsvector columns and GIN indexes must exist)

## Conventions

- **Error handling**: Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `Result<T, AppError>` with `.context()` scope.
- **Response types**: Applies: task modifies `modules/search/src/service/mod.rs` and `modules/search/src/endpoints/mod.rs` matching the convention's `PaginatedResults<T>` scope.
- **Query helpers**: Applies: task modifies `common/src/db/query.rs` matching the convention's shared filtering/pagination/sorting scope.
- **Testing**: Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope.
