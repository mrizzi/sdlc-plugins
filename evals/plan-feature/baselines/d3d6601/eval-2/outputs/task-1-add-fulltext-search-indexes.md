## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates PostgreSQL full-text search indexes on the SBOM, advisory, and package tables. This is the foundational step for improving search performance and relevance (TC-9002). The migration adds tsvector columns and GIN indexes to enable efficient full-text search across all searchable entities.

**Ambiguity note:** The feature description does not specify which fields should be indexed for search. **Assumption pending clarification:** We index the following fields based on analysis of the existing entity structures:
- `sbom`: name and document-level metadata fields
- `advisory`: title, description, and severity fields
- `package`: name and license fields

These field choices may need adjustment once the product owner clarifies which fields users expect to search across.

## Files to Modify
- `entity/src/sbom.rs` — add tsvector column to SBOM entity definition
- `entity/src/advisory.rs` — add tsvector column to Advisory entity definition
- `entity/src/package.rs` — add tsvector column to Package entity definition

## Files to Create
- `migration/src/m0002_add_fulltext_search_indexes/mod.rs` — migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables
- `migration/src/lib.rs` — register the new migration module (modify existing)

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration module structure
- Use SeaORM's migration framework for schema changes — the existing migration in `m0001_initial` demonstrates the pattern
- Create tsvector columns using `ts_vector` type with `english` text search configuration
- Add GIN indexes on the tsvector columns for performant full-text search: `CREATE INDEX idx_sbom_fts ON sbom USING GIN(search_vector)`
- Add a trigger function to automatically update tsvector columns when the source text columns change, using `tsvector_update_trigger` or a custom PL/pgSQL function
- Reference the existing entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to identify the correct column names to include in the tsvector
- Per docs/constraints.md §2 (Commit Rules): use Conventional Commits format with Jira issue ID in footer
- Per docs/constraints.md §5 (Code Change Rules): inspect existing migration code before modifying

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern demonstrating SeaORM migration structure, table creation, and index creation
- `entity/src/sbom.rs` — existing SBOM entity definition showing SeaORM model conventions

## Acceptance Criteria
- [ ] Migration creates tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] Trigger functions automatically populate tsvector columns from source text columns
- [ ] Migration runs successfully against a clean database
- [ ] Migration runs successfully against an existing database (upgrade path)
- [ ] Existing integration tests in `tests/api/` continue to pass (no regression)

## Test Requirements
- [ ] Migration up/down works correctly (can apply and roll back)
- [ ] Verify tsvector columns are populated after inserting test data
- [ ] Verify GIN indexes exist using `\di` or equivalent query
- [ ] All existing tests in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` pass without modification

## Verification Commands
- `cargo test --test api` — all existing integration tests pass
- `sqlx migrate run` — migration applies cleanly

## Dependencies
- None (this is the first task)

[sdlc-workflow] Description digest: sha256:e6bdc945b5b87b94d617b22f11f280e7fd61c7559f69f2fb7afb6e09628335f2
