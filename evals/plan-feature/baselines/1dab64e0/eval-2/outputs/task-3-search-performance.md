## Repository
trustify-backend

## Target Branch
main

## Description
Optimize search performance by adding database indexes for full-text search and improving query patterns in the SearchService. The feature description (TC-9002) states search is "currently too slow" and needs to be faster. This task adds a database migration to create indexes that support efficient full-text search queries and optimizes the SearchService query construction to ensure index utilization.

**Ambiguity note:** The feature description provides no performance baseline or target (e.g., current latency, acceptable latency threshold). This task assumes performance improvement will be validated by ensuring proper index utilization and measuring query execution time before and after the changes, pending clarification from the feature owner on specific performance targets.

## Files to Modify
- `modules/search/src/service/mod.rs` — optimize search query construction to ensure proper index utilization; avoid sequential scans on large tables
- `tests/api/search.rs` — add integration tests to verify search returns results correctly after index changes

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — new migration to create GIN or GiST indexes on full-text search columns across SBOM, advisory, and package tables

## Implementation Notes
Create a new database migration in `migration/src/m0002_search_indexes/mod.rs` following the pattern established in `migration/src/m0001_initial/mod.rs`. The migration should add GIN indexes on the text search vector columns used by the SearchService for full-text search across the SBOM, advisory, and package entities.

Register the new migration module in `migration/src/lib.rs` so it is included in the migration sequence.

Review the current query patterns in `modules/search/src/service/mod.rs` and optimize them to:
1. Use parameterized `to_tsquery` / `plainto_tsquery` for full-text search instead of LIKE or ILIKE patterns if currently used
2. Ensure queries are structured to hit the newly created indexes
3. Avoid `SELECT *` patterns that prevent index-only scans where applicable

The entity definitions in `entity/src/` (specifically `sbom.rs`, `advisory.rs`, `package.rs`) define the SeaORM entities. Review these to identify which columns are used for search and should be indexed.

Per CONVENTIONS.md §Module Pattern: follow the model/ + service/ + endpoints/ structure for the search module.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.

Per CONVENTIONS.md §Error Handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's `.rs` handler file scope.

Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)` pattern.
Applies: task modifies `tests/api/search.rs` matching the convention's `.rs` test file scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — established migration pattern to follow for the new index migration; review for SeaORM migration structure and `Index::create()` usage
- `entity/src/sbom.rs` — SBOM entity definition; identifies which columns are searchable and should be indexed
- `entity/src/advisory.rs` — advisory entity definition; identifies searchable columns
- `entity/src/package.rs` — package entity definition; identifies searchable columns
- `common/src/db/query.rs::query builder helpers` — existing query utilities; review to ensure optimized queries compose correctly with these helpers

## Acceptance Criteria
- [ ] A new database migration creates appropriate indexes for full-text search on SBOM, advisory, and package tables
- [ ] The migration runs successfully against an existing database without data loss
- [ ] The migration is reversible (includes a down/rollback implementation)
- [ ] SearchService queries are optimized to utilize the new indexes
- [ ] All existing search tests continue to pass without modification
- [ ] Search queries with indexes perform measurably better than without (validated by EXPLAIN ANALYZE or equivalent)

## Test Requirements
- [ ] Integration test: migration applies cleanly to a fresh database
- [ ] Integration test: search returns correct results after index migration (verifies indexes do not change query semantics)
- [ ] Integration test: existing search functionality is preserved (regression test)

## Verification Commands
- `cargo test --test search` — run search integration tests, expected: all tests pass
- `sqlx migrate run` or equivalent — run migrations, expected: migration applies without errors
