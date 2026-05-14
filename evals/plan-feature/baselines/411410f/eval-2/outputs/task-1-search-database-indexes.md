# Task 1: Add Database Indexes for Search Performance

## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes to improve search query performance. The current search (TC-9002) is reported as "too slow," but no baseline metrics or targets are provided. This task addresses the structural prerequisite for faster search by adding full-text search indexes and composite indexes on commonly queried columns across the SBOM, advisory, and package entities.

**Assumption (pending clarification)**: The performance bottleneck is assumed to be at the database query level (missing indexes on text-searchable columns), not at the application layer or network layer. No profiling data was provided in the feature description to confirm this. If profiling reveals the bottleneck is elsewhere, this task may need to be re-scoped.

**Assumption (pending clarification)**: PostgreSQL GIN indexes with `tsvector` columns are assumed to be the appropriate full-text search mechanism. The feature description does not specify whether an external search engine (e.g., Elasticsearch, Meilisearch) should be used instead.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New SeaORM migration adding full-text search indexes and composite indexes for search-relevant columns

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module `m0002_search_indexes`
- `entity/src/sbom.rs` — Add index annotations or comments documenting the new indexes on name/description columns
- `entity/src/advisory.rs` — Add index annotations or comments documenting the new indexes on title/description/severity columns
- `entity/src/package.rs` — Add index annotations or comments documenting the new indexes on name/namespace/license columns

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and naming conventions.
- The migration should create GIN indexes on `tsvector` columns for full-text search on:
  - `sbom` table: name and description fields
  - `advisory` table: title, description, and severity fields (severity is referenced in `modules/fundamental/src/advisory/model/summary.rs` as a field on `AdvisorySummary`)
  - `package` table: name, namespace, and license fields (license is referenced in `modules/fundamental/src/package/model/summary.rs` and `entity/src/package_license.rs`)
- Add a composite B-tree index on `advisory.severity` for filter queries (Task 4 will add severity filtering).
- Add a composite B-tree index on `package.license` via the `package_license` join table for license-based filtering.
- The migration must be idempotent — use `IF NOT EXISTS` guards.
- Register the migration in `migration/src/lib.rs` following the pattern used for `m0001_initial`.

## Acceptance Criteria
- [ ] New migration `m0002_search_indexes` is created and registered in `migration/src/lib.rs`
- [ ] GIN full-text indexes exist on text-searchable columns for sbom, advisory, and package tables
- [ ] B-tree indexes exist on `advisory.severity` and package license columns
- [ ] Migration runs successfully against a clean database and against a database with `m0001_initial` already applied
- [ ] Existing search functionality is not broken (search endpoint still returns results)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (verified by running `cargo test` which sets up the test database)
- [ ] Migration applies cleanly on top of existing `m0001_initial` migration
- [ ] Existing tests in `tests/api/search.rs` continue to pass after migration is applied

## Dependencies
- Depends on: None
