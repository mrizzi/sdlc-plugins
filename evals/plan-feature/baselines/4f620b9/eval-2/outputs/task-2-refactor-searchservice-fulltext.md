## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the SearchService to use PostgreSQL full-text search (tsvector/tsquery) with ts_rank for relevance-based result ranking. This replaces the existing search mechanism with proper full-text search capabilities, addressing the "results should be more relevant" requirement from TC-9002.

**Ambiguity note:** The feature does not define what "relevant" means. This task assumes relevance is determined by PostgreSQL's built-in `ts_rank` scoring over tsvector/tsquery matches. If domain-specific relevance weighting is needed (e.g., boosting advisories with critical severity), this should be specified by the product owner as a follow-up.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor SearchService to use tsvector/tsquery with ts_rank ranking
- `modules/search/src/endpoints/mod.rs` — update endpoint handler to pass search query for full-text processing

## Implementation Notes
- Refactor `SearchService` in `modules/search/src/service/mod.rs` to construct `tsquery` from user input and query against the tsvector columns created by the migration task.
- Use `ts_rank(tsvector_column, query)` to score and order results by relevance.
- Use `plainto_tsquery` or `websearch_to_tsquery` for user-friendly query parsing (handles phrases, implicit AND).
- Maintain backward compatibility: if no search query is provided, fall back to listing all entities (existing behavior).
- Return results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs` to maintain the existing response contract.
- Use error handling pattern `Result<T, AppError>` with `.context()` as established in the codebase (see `common/src/error.rs`).
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3 (PR Rules): branch must be named after the Jira issue ID; after opening a PR, post its link as a comment on the Jira task.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend rather than rewrite
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper to maintain consistent response shape
- `common/src/error.rs` — `AppError` enum for consistent error handling
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` demonstrates the service pattern (fetch, list) for reference
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` includes a `search` method that may contain existing search logic to reuse or extend

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL full-text search (tsvector/tsquery) instead of the previous search mechanism
- [ ] Search results are ranked by relevance using ts_rank
- [ ] Empty or missing search query returns all entities (backward compatibility)
- [ ] Response format remains `PaginatedResults<T>` (no breaking API changes)
- [ ] Errors are handled using the established `AppError` pattern

## Test Requirements
- [ ] Integration test: search with a specific term returns matching entities ranked by relevance
- [ ] Integration test: search with no query returns all entities (backward compatibility)
- [ ] Integration test: search with a term that matches multiple entity types returns results from all types
- [ ] Integration test: search with a non-matching term returns empty results

## Verification Commands
- `cargo test -p search` — search module compiles and unit tests pass
- `cargo test --test search` — search integration tests pass (in `tests/api/search.rs`)

## Dependencies
- Depends on: Task 1 — Add full-text search indexes (migration must exist before SearchService can query tsvector columns)

[sdlc-workflow] Description digest: sha256-md:3e1d59985b81b25da6d53b37f697d3dfc84ceadeaf03cb6568fe7d96e1a1804b
