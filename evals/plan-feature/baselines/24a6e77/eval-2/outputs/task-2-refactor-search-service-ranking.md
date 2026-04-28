# Task 2 — Refactor SearchService for Weighted Full-Text Search Ranking

## Repository
trustify-backend

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL full-text search with `ts_rank` weighted ranking instead of basic pattern matching. This directly addresses the user complaint that "search doesn't return useful results" by ranking results based on relevance — matches in titles are weighted higher than matches in descriptions, and exact phrase matches score higher than partial word matches.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace current search query logic with `to_tsquery` + `ts_rank` based full-text search with configurable field weights
- `modules/search/src/lib.rs` — update module exports if new types are introduced

## Implementation Notes
- Inspect the current `SearchService` implementation in `modules/search/src/service/mod.rs` to understand the existing query pattern before modifying
- Use PostgreSQL `to_tsquery('english', <search_term>)` for query parsing and `ts_rank(tsvector_column, tsquery)` for relevance scoring
- Apply field-level weights using `setweight()`: title fields get weight A (highest), description fields get weight B, other fields get weight C
- Use the `plainto_tsquery` variant for user-friendly input parsing (handles spaces, no special syntax required from users), with optional `websearch_to_tsquery` for advanced users
- Follow the existing error handling pattern: `Result<T, AppError>` with `.context()` wrapping (see `common/src/error.rs`)
- Return results ordered by `ts_rank` descending so most relevant results appear first
- Reuse `PaginatedResults<T>` from `common/src/model/paginated.rs` for response structure
- Per constraints doc section 2: commit must reference TC-9002 in footer, use Conventional Commits format
- Per constraints doc section 5: do not modify files outside the scope of this task

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend rather than duplicate query construction logic
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper already used by all list endpoints
- `common/src/error.rs` — `AppError` enum with `IntoResponse` implementation for error handling

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL full-text search (`to_tsquery` / `ts_rank`) instead of basic pattern matching
- [ ] Search results are ordered by relevance score (highest first)
- [ ] Title matches rank higher than description matches
- [ ] Search continues to return results as `PaginatedResults<T>`
- [ ] Existing search endpoint contract is preserved (no breaking API changes)

## Test Requirements
- [ ] Integration test: search for a term that appears in an SBOM title returns that SBOM ranked higher than one where the term only appears in description
- [ ] Integration test: search returns paginated results with correct total count
- [ ] Integration test: search with no matches returns empty results (not an error)
- [ ] Integration test: search handles special characters in query without error

## Verification Commands
- `cargo test -p search` — search module tests pass
- `cargo test --test search` — search integration tests in `tests/api/search.rs` pass

## Dependencies
- Depends on: Task 1 — Add Full-Text Search Indexes via Database Migration
