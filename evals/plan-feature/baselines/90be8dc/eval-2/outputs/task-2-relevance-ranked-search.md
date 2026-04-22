## Repository
trustify-backend

## Description
Refactor the `SearchService` in the search module to use PostgreSQL full-text search with relevance ranking instead of basic string matching. This directly addresses the "results should be more relevant" requirement by scoring results using `ts_rank` and returning them ordered by relevance score.

**Assumption pending clarification:** "Relevant" is interpreted as PostgreSQL `ts_rank` scoring over tsvector columns. The product owner should confirm whether other ranking signals (recency, severity, popularity) should also factor into relevance.

## Files to Modify
- `modules/search/src/service/mod.rs` — Rewrite search queries to use `to_tsquery` against the `search_vector` columns added in Task 1, compute `ts_rank` scores, and order results by score descending
- `common/src/db/query.rs` — Add shared helper functions for building full-text search queries (`to_tsquery` construction, `ts_rank` computation) that can be reused by other modules

## Implementation Notes
The current `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Replace the existing query logic with:

1. Parse the user's search input into a `tsquery` using `plainto_tsquery` or `websearch_to_tsquery` (prefer `websearch_to_tsquery` for better handling of natural language queries).
2. Match against the `search_vector` column on each entity table (`sbom`, `advisory`, `package`).
3. Compute `ts_rank(search_vector, query)` and include it in the result set.
4. Order results by rank descending, with ties broken by creation date.
5. Use the shared query helpers in `common/src/db/query.rs` for constructing these queries — add new helpers there for `ts_rank` and `tsquery` construction so other modules can reuse them.
6. Follow the existing error handling pattern: return `Result<T, AppError>` with `.context()` wrapping, as defined in `common/src/error.rs`.

## Reuse Candidates
- `common/src/db/query.rs::*` — Existing shared query builder helpers for filtering, pagination, sorting; extend with full-text search helpers
- `common/src/model/paginated.rs::PaginatedResults` — Use for paginated search results
- `common/src/error.rs::AppError` — Error handling pattern

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (`tsvector`/`tsquery`) instead of basic string matching
- [ ] Results are ranked by `ts_rank` relevance score, highest first
- [ ] Search spans SBOMs, advisories, and packages
- [ ] Empty or whitespace-only queries return an appropriate error or empty result set
- [ ] Performance improvement is measurable: queries against indexed columns use index scans (verifiable via EXPLAIN)

## Test Requirements
- [ ] Search for a known term returns matching results ordered by relevance
- [ ] Search for a term present in multiple entity types returns results from all types
- [ ] Search for a non-existent term returns an empty result set
- [ ] Partial word matches work as expected (or behavior is documented)

## Verification Commands
- `cargo test -p search` — Unit/integration tests pass
- `cargo clippy -p search` — No linting warnings

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration
