## Repository
trustify-backend

## Description
Add a database migration that creates full-text search indexes on searchable columns to improve search query performance. This is the foundational task that enables the performance and relevance improvements in subsequent tasks. The migration adds PostgreSQL tsvector columns and GIN indexes to the SBOM, advisory, and package tables so that full-text search queries can use index scans instead of sequential scans.

**ASSUMPTION -- pending clarification**: The specific columns to index are assumed to be the name/title and description fields on each entity. This needs validation once "relevant results" is defined by the product owner.

## Files to Modify
- `migration/src/lib.rs` -- Register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` -- New migration that adds tsvector columns and GIN indexes to the sbom, advisory, and package tables for full-text search

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and naming conventions.
- The migration module must be registered in `migration/src/lib.rs` alongside the existing `m0001_initial` module.
- Use PostgreSQL `tsvector` and `GIN` index types for full-text search support. Create a generated tsvector column (or a trigger-maintained column) on each searchable table.
- The entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` define the current table schemas -- review these to identify which text columns should be included in the tsvector.
- Ensure the migration is idempotent and includes both `up` and `down` methods.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` -- Reference for migration structure, SeaORM migration trait implementation, and SQL execution patterns

## Acceptance Criteria
- [ ] New migration module exists at `migration/src/m0002_search_indexes/mod.rs`
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] Migration creates tsvector columns on sbom, advisory, and package tables
- [ ] Migration creates GIN indexes on the tsvector columns
- [ ] Migration includes a `down` method that drops the indexes and columns
- [ ] Migration runs successfully against a clean database and against a database with existing data

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (verified by running the full migration suite)
- [ ] Migration applies cleanly on a database that already has data in the sbom, advisory, and package tables (tsvector columns are populated from existing data)
- [ ] Migration rollback (`down`) executes without errors

## Verification Commands
- `cargo run --bin migration -- up` -- Migration applies without errors
- `cargo run --bin migration -- down` -- Migration rolls back without errors
