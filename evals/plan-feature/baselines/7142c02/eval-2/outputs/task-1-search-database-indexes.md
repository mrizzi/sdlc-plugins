## Repository
trustify-backend

## Target Branch
main

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": "Normal", "fixVersions": ["RHTPA 1.6.0"]}

## Description
Add database migration to create full-text search indexes on searchable columns across SBOM, advisory, and package entities. This is the foundational performance improvement for TC-9002 ("Improve search experience"). The current search is reported as "too slow," and adding proper indexes is the first step before optimizing query patterns.

**Assumption (pending clarification):** No quantitative performance targets were provided in the feature description. This task adds indexes on the columns most likely used for full-text search (name, title, description fields) based on the existing entity definitions. The actual columns may need adjustment once the feature owner clarifies which fields users search most frequently.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration module that creates GIN indexes for full-text search on SBOM, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration list
- `entity/src/sbom.rs` — Verify and document which columns are indexed for search (no schema changes, annotation only if needed)
- `entity/src/advisory.rs` — Verify and document which columns are indexed for search
- `entity/src/package.rs` — Verify and document which columns are indexed for search

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and registration.
- Create PostgreSQL GIN indexes using `tsvector` columns or expression indexes on text columns (e.g., `CREATE INDEX idx_sbom_search ON sbom USING GIN (to_tsvector('english', name || ' ' || coalesce(description, '')))`).
- Register the new migration in `migration/src/lib.rs` following the pattern used for `m0001_initial`.
- Per CONVENTIONS.md §Module pattern: follow the existing module structure for the migration directory. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` module scope.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for any fallible migration operations. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] A new SeaORM migration exists that creates GIN full-text search indexes on searchable text columns in the SBOM, advisory, and package tables
- [ ] The migration is registered in `migration/src/lib.rs` and runs successfully against a PostgreSQL database
- [ ] The migration is reversible (implements both up and down)
- [ ] Existing data is not affected — the migration only adds indexes, no schema changes

## Test Requirements
- [ ] Migration runs successfully on a fresh database (up migration)
- [ ] Migration rolls back successfully (down migration)
- [ ] Existing search endpoint `GET /api/v2/search` continues to function after migration
- [ ] Verify indexes exist in the database after migration using `\di` or equivalent query

## Verification Commands
- `cargo test -p migration` — migration compiles and any migration-specific tests pass

[sdlc-workflow] Description digest: sha256-md:a23f5ab0422c454741f773513bad76caee4f32a6ad84aa22c5938d398bff30dd
