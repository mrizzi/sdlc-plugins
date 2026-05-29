## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates full-text search indexes on searchable columns across the SBOM, Advisory, and Package entities. This migration enables PostgreSQL full-text search capabilities that the SearchService will use to improve search relevance and performance.

**Ambiguity note:** The feature description (TC-9002) does not specify which fields should be searchable or what performance targets are expected. This task assumes that the primary searchable fields are name/title and description columns on each entity, based on the existing entity definitions in `entity/src/`. The product owner should confirm the target field set.

## Files to Create
- `migration/src/m0002_full_text_search_indexes/mod.rs` — Migration to add GIN indexes for full-text search on SBOM, Advisory, and Package entity columns

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure and SeaORM migration trait implementation.
- Create `tsvector` columns or GIN indexes on text columns used for search across the SBOM entity (`entity/src/sbom.rs`), Advisory entity (`entity/src/advisory.rs`), and Package entity (`entity/src/package.rs`).
- Use PostgreSQL `to_tsvector('english', column)` for generating text search vectors, and create GIN indexes on these vectors for efficient full-text search.
- Reference the migration runner registration pattern in `migration/src/lib.rs` to add the new migration to the ordered migration list.
- The migration should be idempotent — use `IF NOT EXISTS` guards where applicable.

**Assumption (pending clarification):** The specific columns to index are assumed based on entity struct inspection. The product owner should confirm which fields users expect to search against.

## Acceptance Criteria
- [ ] A new migration file exists at `migration/src/m0002_full_text_search_indexes/mod.rs`
- [ ] The migration creates GIN indexes for full-text search on SBOM, Advisory, and Package text columns
- [ ] The migration is registered in `migration/src/lib.rs`
- [ ] The migration runs successfully against a PostgreSQL database without errors
- [ ] The migration is idempotent — running it twice does not produce errors

## Test Requirements
- [ ] Verify the migration applies cleanly to a fresh database
- [ ] Verify the migration applies cleanly to an existing database with the initial migration already applied
- [ ] Verify that the created indexes exist after migration by querying `pg_indexes`

## Dependencies
- None

[sdlc-workflow] Description digest: sha256:a83f29fc6ba658ccc204e2ae1830414dcb1fa1e8b34cd56c6fe46313396e4a9a
