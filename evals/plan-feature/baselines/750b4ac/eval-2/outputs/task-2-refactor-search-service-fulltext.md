# Task 2 — Refactor SearchService to use PostgreSQL full-text search with relevance ranking

## Repository
trustify-backend

## Target Branch
main

## Description
Refactor the `SearchService` in `modules/search/src/service/mod.rs` to use PostgreSQL `ts_vector`/`ts_query` full-text search with `ts_rank` relevance scoring. This replaces any existing naive text matching (e.g., LIKE/ILIKE queries) with proper full-text search, directly addressing the "results should be more relevant" requirement from TC-9002. Results will be ordered by relevance score by default.

**Assumption pending clarification:** The relevance ranking model is assumed to be PostgreSQL's built-in `ts_rank` function with default weights. No custom ranking algorithm or field-weighting scheme has been specified in the feature requirements. If specific field weighting is desired (e.g., title matches ranked higher than description matches), this should be clarified with the team.

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor SearchService to use `ts_query` against the tsvector columns added in Task 1, apply `ts_rank` for relevance scoring, and order results by rank
- `modules/search/src/endpoints/mod.rs` — update the `GET /api/v2/search` endpoint handler to pass search terms as `ts_query` and include relevance score in the response
- `common/src/db/query.rs` — add shared full-text search query builder helper that constructs `ts_query` from user input and applies `ts_rank` ordering

## API Changes
- `GET /api/v2/search` — MODIFY: search query parameter now uses PostgreSQL full-text search internally; response includes a `relevance_score` field per result; results are ordered by relevance by default

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` provides "full-text search across entities" — inspect this code to understand the current query mechanism before refactoring. Preserve the existing public API contract where possible.
- Use SeaORM's raw query or expression capabilities to construct `to_tsquery()` from user input and `ts_rank()` for scoring. Sanitize user input to prevent tsquery syntax errors.
- Follow the query builder pattern in `common/src/db/query.rs` — add a shared helper for full-text search queries so that other modules can reuse it in the future.
- List endpoints use `PaginatedResults<T>` from `common/src/model/paginated.rs` — ensure the search results continue to use this wrapper.
- The endpoint in `modules/search/src/endpoints/mod.rs` registers routes at `/api/v2/search` — update the handler to use the refactored service.
- All handlers return `Result<T, AppError>` with `.context()` wrapping from `common/src/error.rs` — maintain this pattern.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits and reference TC-9002 in the footer.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing SearchService code before modifying; do not duplicate utilities already in `common/src/db/query.rs`.

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers for filtering, pagination, and sorting; extend rather than duplicate
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper already used by list endpoints; reuse for search results
- `common/src/error.rs::AppError` — standard error type; use for all error handling in the refactored service
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service with `search` method; inspect for patterns to follow

## Acceptance Criteria
- [ ] SearchService uses PostgreSQL `ts_vector`/`ts_query` for full-text search instead of naive text matching
- [ ] Search results are ranked by relevance using `ts_rank` and ordered by relevance score by default
- [ ] A relevance score is included in each search result
- [ ] The existing `GET /api/v2/search` endpoint continues to work with the same URL pattern
- [ ] Search handles edge cases: empty query, special characters, very long queries
- [ ] A shared full-text search query builder helper is added to `common/src/db/query.rs`

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: verify that a search query returns results ordered by relevance
- [ ] Integration test: verify that more specific queries return more relevant results ranked higher
- [ ] Integration test: verify that empty or malformed search queries return appropriate error responses
- [ ] Integration test: verify that search results include the relevance score field

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search API integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search migration for SBOM, advisory, and package entities

[sdlc-workflow] Description digest: sha256-md:79bf4a06d741c36d8779dc70fcf3687628cf65d7889d41c41e820c3dfaac3f8b
