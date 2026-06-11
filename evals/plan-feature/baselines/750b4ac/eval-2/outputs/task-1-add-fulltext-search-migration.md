# Task 1 — Add full-text search migration for SBOM, advisory, and package entities

## Repository
trustify-backend

## Target Branch
main

## Description
Create a database migration that adds PostgreSQL full-text search indexes (`tsvector` columns and GIN indexes) to the SBOM, advisory, and package tables. This migration enables the backend to perform efficient full-text search with relevance ranking instead of naive text pattern matching, addressing the "search should be faster" and "results should be more relevant" requirements from TC-9002.

**Assumption pending clarification:** The specific text fields to index are assumed based on existing entity structures — SBOM name/description, advisory title/description/severity, and package name/license. The actual field selection should be confirmed with the team.

**Assumption pending clarification:** No measurable performance SLA has been defined for "faster" search. This migration targets structural optimization (GIN indexes for full-text search) with performance validated via integration tests rather than a specific latency threshold.

## Files to Create
- `migration/src/m0002_fulltext_search_indexes/mod.rs` — migration module adding tsvector columns and GIN indexes to sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner
- `entity/src/sbom.rs` — add `search_vector` tsvector column to the SBOM entity definition
- `entity/src/advisory.rs` — add `search_vector` tsvector column to the advisory entity definition
- `entity/src/package.rs` — add `search_vector` tsvector column to the package entity definition

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and SeaORM migration conventions.
- Use PostgreSQL `tsvector` columns with a GIN index on each entity table. Create a trigger or use a generated column to keep the tsvector in sync with source text fields.
- For the SBOM entity (`entity/src/sbom.rs`), index text fields present in `SbomSummary` (`modules/fundamental/src/sbom/model/summary.rs`).
- For the advisory entity (`entity/src/advisory.rs`), index text fields present in `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`), including the severity field.
- For the package entity (`entity/src/package.rs`), index text fields present in `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`), including the license field.
- All handlers in this codebase return `Result<T, AppError>` with `.context()` wrapping — ensure migration errors follow this pattern where applicable.
- Per docs/constraints.md §2 (Commit Rules): commit messages must follow Conventional Commits and reference TC-9002 in the footer.
- Per docs/constraints.md §5 (Code Change Rules): inspect existing migration code before writing new code; do not duplicate existing patterns.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration pattern to follow for structure, table creation, and SeaORM integration
- `common/src/db/query.rs` — shared query builder helpers; may already contain text search patterns to reuse or extend

## Acceptance Criteria
- [ ] A new migration module exists that adds tsvector columns and GIN indexes to sbom, advisory, and package tables
- [ ] The migration is registered in `migration/src/lib.rs` and runs successfully against a PostgreSQL database
- [ ] Entity definitions in `entity/src/` are updated with the new tsvector column
- [ ] The migration is idempotent and can be rolled back cleanly

## Test Requirements
- [ ] Migration runs successfully against the PostgreSQL test database
- [ ] Verify GIN indexes are created by querying `pg_indexes` after migration
- [ ] Verify tsvector columns are populated correctly when test data is inserted

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo build -p entity` — entity crate builds with updated definitions

## Dependencies
- None (first task in the sequence)

[sdlc-workflow] Description digest: sha256-md:7fcd4dd118bdbbd049de5679001017e9dc19dfa7ddb0615080296945028a14a1
