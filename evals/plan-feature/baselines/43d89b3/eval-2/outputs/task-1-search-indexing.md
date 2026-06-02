## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes to improve search query performance. The current search implementation in `SearchService` performs full-text queries without dedicated indexes, leading to slow response times. This task adds PostgreSQL indexes on the columns and expressions used by the search service to accelerate query execution.

**Ambiguity note:** The feature description does not specify current latency baselines or target performance thresholds. **Assumption pending clarification:** We assume the goal is sub-500ms p95 response time for typical search queries. The product owner should confirm specific performance targets.

## Files to Modify
- `migration/src/lib.rs` — register new migration module
- `common/src/db/query.rs` — update query builder helpers to leverage new indexes if needed

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration adding GIN/GiST indexes for full-text search columns on sbom, advisory, and package tables

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. Create a new migration module under `migration/src/` following the sequential naming convention (`m0002_search_indexes`).

The migration should add:
- A GIN index on the full-text search vector column(s) used by `SearchService` in `modules/search/src/service/mod.rs`
- B-tree indexes on commonly filtered columns (created_at, severity) on the `advisory` entity (`entity/src/advisory.rs`) and `sbom` entity (`entity/src/sbom.rs`)

Register the new migration in `migration/src/lib.rs` following the pattern used for `m0001_initial`.

Use SeaORM migration patterns consistent with the project's framework conventions (SeaORM for database, as noted in Key Conventions).

Per docs/constraints.md:
- §2 (Commit Rules): commits must reference TC-9002, follow Conventional Commits, and include the Assisted-by trailer.
- §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes.

## Reuse Candidates
- `common/src/db/query.rs::query builder helpers` — existing query builder infrastructure that may need awareness of new indexes for query plan optimization
- `migration/src/m0001_initial/mod.rs` — migration pattern to follow for the new migration module

## Acceptance Criteria
- [ ] New migration module `m0002_search_indexes` is created and registered
- [ ] GIN index is added for full-text search columns used by SearchService
- [ ] B-tree indexes are added for commonly filtered columns (created_at, severity)
- [ ] Migration runs successfully against a PostgreSQL test database
- [ ] Existing search functionality is not broken (all existing tests pass)

## Test Requirements
- [ ] Migration applies cleanly to a fresh database
- [ ] Migration applies cleanly to an existing database with data
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass after migration
- [ ] Existing integration tests in `tests/api/sbom.rs` and `tests/api/advisory.rs` continue to pass

## Verification Commands
- `cargo test --test search` — existing search tests pass
- `cargo test --test sbom` — existing SBOM tests pass
- `cargo test --test advisory` — existing advisory tests pass
