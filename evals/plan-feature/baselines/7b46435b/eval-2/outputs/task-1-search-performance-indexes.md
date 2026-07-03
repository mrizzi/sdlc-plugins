## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration to add PostgreSQL GIN indexes on text columns used by the search service, improving full-text search query performance. This task addresses the "search should be faster" requirement from TC-9002 by adding database-level indexing that enables PostgreSQL to use optimized full-text search operations instead of sequential scans.

**Assumption pending clarification:** The performance improvement target is not specified in the feature description. This migration adds GIN indexes as a standard approach to improving full-text search performance. Specific latency SLAs should be defined by the product owner to validate whether this improvement is sufficient.

additional_fields: { "labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": "RHTPA 1.6.0" }

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- migration that creates GIN indexes on searchable text columns across SBOM (name/description), advisory (title/description), and package (name) entities using `tsvector` columns and GIN index type

## Files to Modify
- `migration/src/lib.rs` -- register the new migration module `m0002_search_indexes` in the migration list

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for the migration module structure and SeaORM migration trait implementation.

The migration should:
1. Add `tsvector` generated columns to the `sbom`, `advisory`, and `package` tables that combine their searchable text fields
2. Create GIN indexes on these `tsvector` columns using `CREATE INDEX ... USING GIN(...)` via raw SQL in the migration's `up` method
3. The `down` method should drop the indexes and the generated columns

Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` for the exact column names to index.

Per CONVENTIONS.md: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` module scope.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- existing migration module; follow the same migration trait implementation pattern and module registration approach
- `entity/src/sbom.rs` -- SBOM entity definition with column names for indexing
- `entity/src/advisory.rs` -- Advisory entity definition with column names for indexing
- `entity/src/package.rs` -- Package entity definition with column names for indexing

## Acceptance Criteria
- [ ] Migration creates GIN indexes on searchable text columns for SBOM, advisory, and package entities
- [ ] Migration adds `tsvector` generated columns for full-text search on the relevant tables
- [ ] Migration `up` and `down` methods are both implemented and reversible
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Existing integration tests pass without regression after migration

## Test Requirements
- [ ] Migration applies successfully on a clean database
- [ ] Migration rolls back cleanly (down method works)
- [ ] Existing search endpoint tests in `tests/api/search.rs` continue to pass after migration

## Verification Commands
- `cargo build -p trustify-migration` -- compiles without errors
- `cargo test -p trustify-migration` -- migration tests pass

## Dependencies
- None (this is the foundational task)
