## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration to create GIN indexes on tsvector columns for full-text search capability across SBOMs, advisories, and packages. This migration lays the foundation for PostgreSQL full-text search by adding the necessary tsvector columns and GIN indexes that will be used by the refactored SearchService in a subsequent task.

**Ambiguity note:** The feature TC-9002 does not specify which fields should be searchable or what "faster" means quantitatively. This task assumes that full-text search indexing on name/description fields of the three core entities (SBOMs, advisories, packages) is the intended scope. Validate with the product owner which fields should be indexed.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module

## Files to Create
- `migration/src/m0002_fulltext_search_indexes/mod.rs` — migration to add tsvector columns and GIN indexes to sbom, advisory, and package tables

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration trait implementation.
- Create tsvector columns on the `sbom`, `advisory`, and `package` tables using `ALTER TABLE ... ADD COLUMN ... tsvector`.
- Create GIN indexes on the new tsvector columns using `CREATE INDEX ... USING gin(...)`.
- Add a trigger or use `GENERATED ALWAYS AS` to keep tsvector columns in sync with source text columns (name, description, etc.).
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`.
- Per docs/constraints.md §3 (PR Rules): branch must be named after the Jira issue ID; after opening a PR, post its link as a comment on the Jira task.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the SeaORM migration pattern (struct, up/down methods)

## Acceptance Criteria
- [ ] A new migration module exists that adds tsvector columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on the tsvector columns
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] Migration runs successfully against a PostgreSQL test database (up and down)

## Test Requirements
- [ ] Migration `up` executes without errors and creates the expected columns and indexes
- [ ] Migration `down` executes without errors and removes the columns and indexes
- [ ] Existing data in sbom, advisory, and package tables is preserved after migration

## Verification Commands
- `cargo test -p migration` — migration compiles and tests pass

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:feed1cb8f2536e663f53a345c3ac4a8363e74ddc21e7008088f529c3efe00432
