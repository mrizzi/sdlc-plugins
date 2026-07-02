additional_fields: { "labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": ["RHTPA 1.6.0"] }

## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search query performance by adding PostgreSQL full-text search indexes and tuning the SearchService query implementation. The feature description states search is "currently too slow" but provides no baseline metrics or target latency. This task addresses the MVP requirement "Search should be faster" by adding database-level indexes to accelerate full-text queries and optimizing the query construction in the search service layer.

**Assumption (pending clarification):** "Faster" is interpreted as adding GIN indexes on text columns used by the full-text search and ensuring the SearchService uses indexed `tsvector` columns rather than unindexed `LIKE`/`ILIKE` patterns. Without defined performance targets, the goal is to ensure search queries use index scans rather than sequential scans.

**Ambiguity:** The feature specifies no quantitative performance targets (e.g., p95 latency < 200ms, support for N concurrent queries). The implementation focuses on structural improvements (indexes, query optimization) that provide measurable gains regardless of the specific target.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- Migration to add GIN indexes on searchable text columns across sbom, advisory, and package entities for full-text search acceleration

## Files to Modify
- `migration/src/lib.rs` -- Register the new m0002_search_indexes migration module
- `modules/search/src/service/mod.rs` -- Optimize SearchService query construction to leverage the new full-text indexes; replace any unindexed pattern matching with tsvector/tsquery operations

## Implementation Notes
- Follow the existing migration module pattern established in `migration/src/m0001_initial/mod.rs`. Create a new migration directory `m0002_search_indexes/` with a `mod.rs` containing the index creation statements.
- The migration should add GIN indexes on text columns in the `sbom`, `advisory`, and `package` entity tables that the SearchService queries. Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the searchable columns.
- In `modules/search/src/service/mod.rs`, update the SearchService's full-text search implementation to use PostgreSQL `to_tsvector` / `to_tsquery` with the GIN indexes rather than `LIKE` or `ILIKE` patterns.
- Use the shared query builder helpers from `common/src/db/query.rs` for constructing the optimized queries, following the existing patterns for filtering and pagination.
- All database interactions must return `Result<T, AppError>` with `.context()` wrapping per the project error handling convention.
- Per CONVENTIONS.md: follow the module pattern (model/ + service/ + endpoints/) and use SeaORM for all database operations.
  Applies: task modifies `modules/search/src/service/mod.rs` and creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` -- Shared query builder helpers for filtering, pagination, and sorting; reuse for constructing optimized search queries
- `common/src/error.rs::AppError` -- Project error enum with IntoResponse; use for all error returns in the migration and service changes

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` creates GIN indexes on all text columns used by the search service
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] SearchService in `modules/search/src/service/mod.rs` uses tsvector/tsquery operations that leverage the new indexes
- [ ] Search queries produce EXPLAIN plans showing index scans (not sequential scans) on indexed columns
- [ ] Existing search functionality continues to return correct results (no regression)

## Test Requirements
- [ ] Add integration test in `tests/api/search.rs` verifying that search queries return results after index migration is applied
- [ ] Add integration test confirming search returns results for partial-match and full-match queries using the new full-text search implementation
- [ ] Verify the migration runs successfully against the test PostgreSQL database without errors

## Verification Commands
- `cargo test --test search` -- All search integration tests pass
- `cargo run --bin migration` -- Migration applies cleanly to the database

## Dependencies
- None (this is the foundational task)
