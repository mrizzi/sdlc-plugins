# Task 2 — Implement relevance scoring for search results

**Feature:** TC-9002 — Improve search experience
**Label:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
main

## Description
Users report that search results are not useful — relevant items are buried among irrelevant matches. This task implements relevance-based ranking in the search service so that results are ordered by how well they match the query, rather than by insertion order or arbitrary sorting. This addresses the "results should be more relevant" requirement.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add relevance scoring logic to `SearchService` that computes a match score based on PostgreSQL `ts_rank` or `ts_rank_cd` functions, and orders results by score descending
- `modules/search/src/endpoints/mod.rs` — Update the `GET /api/v2/search` endpoint handler to pass ranking configuration to the service and expose the relevance score in the response
- `common/src/db/query.rs` — Add a ranking/ordering helper that supports `ORDER BY ts_rank(...)` so the search module can use it via the shared query builder

## API Changes
- `GET /api/v2/search` — MODIFY: Response items now include an optional `relevance_score: f32` field. Results are ordered by relevance score descending by default. A new optional query parameter `sort=relevance|date|name` controls sort order.

## Implementation Notes
- **Ranking approach:** Use PostgreSQL's built-in `ts_rank` or `ts_rank_cd` functions operating on the `tsvector` columns and indexes created in Task 1. Weight different fields (e.g., title matches ranked higher than description matches) using the weight parameter of `ts_rank`.
- **Response wrapper:** Use `PaginatedResults<T>` from `common/src/model/paginated.rs` for the response. The individual result items should be extended with a `relevance_score` field. Look at how `SbomSummary`, `AdvisorySummary`, and `PackageSummary` are structured in their respective `model/summary.rs` files for the established pattern.
- **Error handling:** Follow the `Result<T, AppError>` pattern with `.context()` wrapping, as used throughout the codebase.
- **Endpoint registration:** The search endpoint is registered in `modules/search/src/endpoints/mod.rs`. Follow the route registration pattern used by other modules (e.g., `modules/fundamental/src/sbom/endpoints/mod.rs`).
- **Constraint §5.2:** Inspect `SearchService` in `modules/search/src/service/mod.rs` before modifying it.
- **Constraint §5.4:** Extend the shared query builder in `common/src/db/query.rs` for ranking support rather than embedding raw SQL in the search module.
- **Constraint §5.8:** Compare the search endpoint implementation against sibling endpoints (`sbom/endpoints/list.rs`, `advisory/endpoints/list.rs`) for parity on error handling, pagination, and response structure.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — Extend with ranking/ordering support rather than writing custom ORDER BY logic
- `common/src/model/paginated.rs::PaginatedResults<T>` — Use for paginated, ranked search results
- `modules/fundamental/src/sbom/model/summary.rs::SbomSummary` — Reference as a pattern for how to structure result item types with additional fields
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference for severity field pattern, which is analogous to adding a relevance_score field

## Acceptance Criteria
- [ ] Search results are ordered by relevance score by default
- [ ] Each search result item includes a `relevance_score` field
- [ ] A `sort` query parameter allows switching between relevance, date, and name ordering
- [ ] Title matches rank higher than description matches
- [ ] Existing search queries that worked before continue to return results

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying that a query matching a document title ranks it above a description-only match
- [ ] Integration test verifying the `sort` parameter produces correct ordering for each value (relevance, date, name)
- [ ] Integration test verifying that the `relevance_score` field is present in response items

## Verification Commands
- `cargo test -p tests --test search` — all search integration tests pass

## Dependencies
- Depends on: Task 1 — Optimize search query performance (requires full-text search indexes and tsvector columns)
