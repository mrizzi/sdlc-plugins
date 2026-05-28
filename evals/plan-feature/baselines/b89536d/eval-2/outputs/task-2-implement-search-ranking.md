# Task 2 — Implement search result relevance ranking in SearchService

## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the SearchService to use PostgreSQL full-text search with relevance ranking instead of the current search approach. Replace or augment existing search queries with `to_tsquery` matching against the tsvector columns added in Task 1, and order results by `ts_rank_cd` score so that more relevant results appear first. This directly addresses the user complaint that "search doesn't return useful results."

## Files to Modify
- `modules/search/src/service/mod.rs` — refactor SearchService to use full-text search with tsvector matching and ts_rank_cd scoring
- `modules/search/src/endpoints/mod.rs` — update the GET /api/v2/search handler to pass ranking parameters and return results ordered by relevance score

## API Changes
- `GET /api/v2/search` — MODIFY: results are now ordered by relevance score (ts_rank_cd) by default; response may include an optional `relevance_score` field per result

## Implementation Notes
- Use `to_tsquery('english', ...)` to parse user search input into a tsquery. Handle multi-word queries by joining terms with `&` (AND) for strict matching.
- Apply `ts_rank_cd(tsvector_column, query)` to compute relevance scores and use it as the ORDER BY clause.
- Fall back to ILIKE-based search when the query is a single character or contains special characters that tsquery cannot parse.
- Reference the existing `SearchService` in `modules/search/src/service/mod.rs` to understand the current search implementation before modifying it.
- Use SeaORM raw query capabilities or `Expr::cust()` to express PostgreSQL-specific full-text search functions that may not have direct SeaORM abstractions.
- Per docs/constraints.md section 2 (Commit Rules): commit must reference TC-9002 in the footer and follow Conventional Commits.
- Per docs/constraints.md section 5 (Code Change Rules): inspect code before modifying; follow patterns in Implementation Notes.

## Reuse Candidates
- `modules/search/src/service/mod.rs` — existing SearchService implementation to extend rather than rewrite
- `common/src/db/query.rs` — shared query builder helpers for pagination and sorting that should be composed with the new ranking logic
- `common/src/model/paginated.rs` — PaginatedResults wrapper used by list endpoints; search results should continue using this wrapper

## Acceptance Criteria
- [ ] Search queries use PostgreSQL full-text search (tsquery/tsvector) for matching
- [ ] Results are ordered by relevance score by default
- [ ] Multi-word queries return results matching all terms
- [ ] Single-character and special-character queries still return results (fallback behavior)
- [ ] Existing search functionality is not broken — queries that worked before still return results

## Test Requirements
- [ ] Integration test: search for a known SBOM name returns it as the top result
- [ ] Integration test: multi-word query returns results matching all terms
- [ ] Integration test: search results are ordered by relevance (more specific matches rank higher)
- [ ] Integration test: empty or single-character query returns results without error

## Verification Commands
- `cargo test --test api search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search GIN indexes via database migration
