# Task 4 — Ensure search endpoint uses PaginatedResults with sorting support

**Feature:** TC-9002 — Improve search experience
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Description
Verify and ensure that the `GET /api/v2/search` endpoint returns results using the standard `PaginatedResults<T>` response wrapper with proper pagination (offset/limit) and sorting support. The existing list endpoints (SBOMs, advisories, packages) already use this pattern, but the search endpoint may not be fully consistent. This task aligns the search endpoint with the established conventions.

**Ambiguity flag:** The feature does not mention pagination or sorting requirements for search. This task assumes the search endpoint should follow the same pagination and sorting conventions as the existing list endpoints (`GET /api/v2/sbom`, `GET /api/v2/advisory`, `GET /api/v2/package`), which use `PaginatedResults<T>`.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — Ensure the search endpoint accepts `offset`, `limit`, and `sort` query parameters; returns `PaginatedResults<T>`
- `modules/search/src/service/mod.rs` — Ensure `SearchService` supports pagination parameters and sort options (relevance, date, name) in queries

## Implementation Notes
- Inspect the current search endpoint in `modules/search/src/endpoints/mod.rs` to determine whether it already uses `PaginatedResults<T>` — if it does, this task may only need to add sorting options
- Reference the list endpoints in `modules/fundamental/src/sbom/endpoints/list.rs` and `modules/fundamental/src/advisory/endpoints/list.rs` for the established pagination pattern
- Use the shared pagination and sorting helpers from `common/src/db/query.rs` — do not implement custom pagination logic
- The `PaginatedResults<T>` type is defined in `common/src/model/paginated.rs`
- Sort options should include: `relevance` (default, from Task 2), `date`, `name`
- When sorting by relevance, the relevance score from Task 2 determines order
- Per docs/constraints.md Section 5.4: reuse existing pagination utilities; do not duplicate

## Reuse Candidates
- `common/src/db/query.rs` — Shared query helpers for pagination and sorting
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper to reuse
- `modules/fundamental/src/sbom/endpoints/list.rs` — Reference implementation of a paginated list endpoint
- `modules/fundamental/src/advisory/endpoints/list.rs` — Another reference for pagination pattern

## Acceptance Criteria
- [ ] `GET /api/v2/search` returns `PaginatedResults<T>` with `items`, `total` (or equivalent fields)
- [ ] Pagination via `offset` and `limit` query parameters works correctly
- [ ] Sort options (`relevance`, `date`, `name`) are accepted and applied
- [ ] Default sort is by relevance when no sort parameter is provided
- [ ] Response format is consistent with other list endpoints (`/api/v2/sbom`, `/api/v2/advisory`)

## Test Requirements
- [ ] Integration test: search with `offset=0&limit=10` returns at most 10 results with correct total count
- [ ] Integration test: search with `offset=10&limit=10` returns the second page of results
- [ ] Integration test: search with `sort=date` returns results ordered by date
- [ ] Integration test: search with `sort=name` returns results ordered alphabetically by name
- [ ] Integration test: search without sort parameter returns results ordered by relevance (default)

## Verification Commands
- `cargo test -p tests --test search` — search tests pass

## Dependencies
- Depends on: Task 2 — Add field-weighted relevance scoring to search results (relevance score is needed for default sort)
