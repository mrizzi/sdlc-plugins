## Repository
trustify-backend

## Target Branch
main

## Description
Implement weighted full-text search ranking in `SearchService` to improve result relevance. Currently, search results are returned without meaningful ranking, causing users to see irrelevant results. This task adds relevance scoring based on full-text search rank functions and sorts results by relevance score by default.

**Ambiguity note:** The feature description does not define what constitutes "relevant" results. There are no specified ranking factors, no priority ordering of entity types, and no example queries demonstrating poor results. **Assumption pending clarification:** We assume relevance should be determined by PostgreSQL `ts_rank` or `ts_rank_cd` scoring on full-text search vectors, with exact matches weighted higher than partial matches. The product owner should confirm ranking priorities (e.g., whether advisories with higher severity should rank above others).

## Files to Modify
- `modules/search/src/service/mod.rs` — add relevance scoring logic to `SearchService` full-text search queries
- `modules/search/src/endpoints/mod.rs` — add optional `sort_by=relevance` query parameter, default to relevance-based ordering

## Implementation Notes
Modify the `SearchService` in `modules/search/src/service/mod.rs` to:
1. Use PostgreSQL `ts_rank` or `ts_rank_cd` functions to compute a relevance score for each result
2. Order results by relevance score descending by default when no explicit sort is specified
3. Support an optional `sort_by` query parameter to allow sorting by relevance, date, or name

Follow the existing endpoint pattern in `modules/search/src/endpoints/mod.rs` (route registration at `/api/v2/search`). The endpoint already exists; this task extends its query parameter handling.

Use the shared query builder helpers in `common/src/db/query.rs` for sorting and pagination. The existing `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs` should be preserved for response format.

All handlers must return `Result<T, AppError>` with `.context()` wrapping, following the error handling pattern defined in `common/src/error.rs`.

Per docs/constraints.md:
- §2 (Commit Rules): commits must reference TC-9002, follow Conventional Commits, and include the Assisted-by trailer.
- §3 (PR Rules): branch must be named after the Jira issue ID; PR link must be posted to the task.
- §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for sorting and pagination; extend rather than duplicate
- `common/src/model/paginated.rs::PaginatedResults<T>` — existing response wrapper to reuse for paginated search results
- `common/src/error.rs::AppError` — error handling pattern to follow

## Acceptance Criteria
- [ ] Search results are ranked by relevance score by default
- [ ] Exact matches rank higher than partial matches
- [ ] An optional `sort_by` query parameter is supported (values: `relevance`, `date`, `name`)
- [ ] Default sort order is `relevance` when a search query is provided
- [ ] Existing search behavior is preserved when no query is provided (list-style queries use existing sort)
- [ ] Response format remains `PaginatedResults<T>`

## Test Requirements
- [ ] Integration test verifying that exact match queries return the exact match as the first result
- [ ] Integration test verifying that partial match queries return results ordered by relevance score
- [ ] Integration test verifying the `sort_by` query parameter changes result ordering
- [ ] Integration test verifying default sort is relevance when a search term is present
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — all search tests pass including new relevance tests
