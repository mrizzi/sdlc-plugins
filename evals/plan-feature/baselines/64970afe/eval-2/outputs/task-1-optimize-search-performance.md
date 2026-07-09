## Repository
trustify-backend

## Target Branch
main

## Description
Optimize the search query performance in the SearchService to reduce search response latency. The current full-text search implementation needs database-level optimization through appropriate indexes and query execution improvements.

**Ambiguity notice:** The feature description specifies "search should be faster" without quantitative targets. This task assumes a target of p95 < 500ms for queries returning up to 100 results (assumption A1 -- pending clarification from product owner). The non-functional requirement "should be fast enough" is similarly unmeasurable (assumption -- pending clarification on acceptable latency thresholds).

## Files to Modify
- `modules/search/src/service/mod.rs` -- Optimize search query construction to leverage database indexes and reduce query execution time
- `common/src/db/query.rs` -- Add search-optimized query builder methods for full-text search operations

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- Database migration to add GIN indexes on full-text search columns for SBOMs, advisories, and packages

## Implementation Notes
- Analyze the existing SearchService implementation in `modules/search/src/service/mod.rs` to identify query patterns that lack index support
- Add PostgreSQL GIN indexes on text columns used for full-text search (e.g., name and description fields on SBOM, advisory, and package entities defined in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs`)
- Use `tsvector` columns with GIN indexes for PostgreSQL full-text search acceleration
- Leverage the existing query builder helpers in `common/src/db/query.rs` for consistent query construction
- Consider adding query result caching via the existing `tower-http` caching middleware configuration in endpoint route builders
- The migration should follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`
- Register the new migration module in `migration/src/lib.rs`

Per CONVENTIONS.md §Error Handling: all new or modified service methods must return `Result<T, AppError>` with `.context()` wrapping for error propagation. See `common/src/error.rs` for the AppError enum.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` file scope.

Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs` rather than building ad-hoc query logic.
Applies: task modifies `common/src/db/query.rs` matching the convention's query helper scope.

## Reuse Candidates
- `common/src/db/query.rs` -- Existing filtering and pagination utilities that should be extended rather than duplicated for search optimization
- `common/src/db/limiter.rs` -- Existing connection pool management that may need tuning for search workloads
- `migration/src/m0001_initial/mod.rs` -- Reference migration pattern for creating the new index migration

## Acceptance Criteria
- [ ] GIN indexes are created on full-text search columns via a new database migration
- [ ] SearchService query execution leverages the new indexes for full-text search
- [ ] Search query performance is measurably improved (target: p95 < 500ms for typical queries -- assumption A1, pending clarification)
- [ ] Existing search API behavior is preserved (same response shape, all entity types still searchable)
- [ ] Migration runs successfully against a clean database and as an incremental migration

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` verifying search endpoint returns correct results after index migration
- [ ] Integration test verifying search performance does not regress under typical query patterns
- [ ] Migration test verifying indexes are created correctly on target columns

## Verification Commands
- `cargo test --test search` -- Verify search integration tests pass
- `cargo build` -- Verify project compiles without errors

## Dependencies
- None
