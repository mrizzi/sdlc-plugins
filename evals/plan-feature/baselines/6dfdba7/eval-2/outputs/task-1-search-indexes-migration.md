## Repository
trustify-backend

## Description
Create a database migration that adds full-text search indexes to improve search query performance. The current search is reported as "too slow," and adding GIN indexes on tsvector columns for key searchable fields (SBOM names/descriptions, advisory titles/descriptions, package names) will enable PostgreSQL's built-in full-text search capabilities with significantly better performance than LIKE/ILIKE queries.

**Assumption (pending clarification):** This task assumes PostgreSQL full-text search (tsvector/tsquery with GIN indexes) is the desired approach, since no external search engine was specified. If an external search engine (e.g., Elasticsearch) is preferred, this task would need to be redesigned.

**Assumption (pending clarification):** The specific fields to index are assumed to be name/title and description fields on sbom, advisory, and package entities, since the feature does not specify which fields should be searchable.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_indexes migration module

## Implementation Notes
- Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs` — use SeaORM's migration trait implementation
- The migration should:
  1. Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
  2. Create GIN indexes on each `search_vector` column for fast full-text lookups
  3. Create a trigger function that automatically updates the `search_vector` column when rows are inserted or updated, concatenating relevant text fields (e.g., name, description) with appropriate weights (A for title/name, B for description)
  4. Backfill the `search_vector` column for existing rows
- Reference `migration/Cargo.toml` for the existing migration crate dependencies
- The migration must be reversible (implement `down()` to drop the indexes, triggers, and columns)

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Pattern for writing SeaORM migrations with up/down methods

## Acceptance Criteria
- [ ] Migration creates tsvector columns on sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] Trigger functions automatically maintain tsvector columns on insert/update
- [ ] Existing data is backfilled with search vectors
- [ ] Migration is reversible (down migration drops all added objects)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies successfully against a clean database
- [ ] Migration rolls back cleanly
- [ ] After migration, inserting a new SBOM row automatically populates the search_vector column
- [ ] GIN index is used by the query planner for full-text search queries (verify with EXPLAIN)

## Verification Commands
- `cargo test -p migration` — Migration tests pass
