## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates full-text search indexes to improve search query performance. This migration adds PostgreSQL `tsvector` columns and GIN indexes on commonly searched text fields across SBOMs, advisories, and packages. This addresses the TC-9002 requirement that "search should be faster" by enabling PostgreSQL's native full-text search capabilities instead of relying on LIKE/ILIKE queries.

**Assumption (pending clarification):** The specific fields to index are assumed based on the existing entity models. The product owner should confirm which fields are most important for search relevance.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that adds tsvector columns and GIN indexes for full-text search on sbom (name, description), advisory (title, description), and package (name) tables

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration runner

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` for migration structure and registration.
- Use PostgreSQL `tsvector` columns with `GIN` indexes for full-text search. The migration should:
  1. Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables.
  2. Create a `GIN` index on each `search_vector` column.
  3. Create a trigger on each table to automatically update the `search_vector` column when relevant text fields change.
- Use `ts_to_tsvector('english', ...)` with appropriate weights: 'A' weight for title/name fields, 'B' weight for description fields, so title matches rank higher.
- The migration must be reversible (include a down migration that drops the indexes, triggers, and columns).
- Per docs/constraints.md §5.4: Do not duplicate existing functionality — check if any indexing utilities exist in `common/src/db/` before writing new helpers.
- Per docs/constraints.md §2.1-2.3: Commits must reference TC-9002, follow Conventional Commits, and include the AI assistance trailer.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Established migration pattern showing how to structure SeaORM migrations in this project
- `common/src/db/query.rs` — Shared query builder helpers that may already have indexing or search-related utilities

## Acceptance Criteria
- [ ] A new migration exists that adds `tsvector` columns to `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Triggers are created to automatically populate `search_vector` from relevant text fields
- [ ] The migration runs successfully against the test database
- [ ] The migration is reversible (down migration works correctly)
- [ ] Existing data has its `search_vector` columns populated after migration

## Test Requirements
- [ ] Verify the migration runs forward successfully on a clean database
- [ ] Verify the migration can be rolled back (down migration)
- [ ] Verify that inserting a new record populates the `search_vector` column via the trigger
- [ ] Verify that updating a text field updates the `search_vector` column via the trigger

## Verification Commands
- `cargo test -p migration` — migration compiles and any migration-level tests pass
