## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates PostgreSQL full-text search indexes (GIN indexes) on the sbom, advisory, and package tables. This is the foundational step for improving search performance (TC-9002 requirement: "Search should be faster"). The migration creates tsvector columns and GIN indexes to enable efficient full-text search with ranking, replacing any existing naive LIKE/ILIKE queries.

**AMBIGUITY flagged**: The feature does not specify which columns should be indexed or what constitutes "searchable" content per entity. **ASSUMPTION pending clarification**: We index the primary text fields — name/title columns on SBOMs, title/description/severity on advisories, and name/namespace on packages. These are the most likely search targets based on the entity definitions.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables. Includes a trigger to keep tsvector columns updated on INSERT/UPDATE.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module `m0002_search_indexes` in the migration runner

## Implementation Notes
Follow the existing migration pattern established in `migration/src/m0001_initial/mod.rs`. The new migration module should be added under `migration/src/` with its own directory following the `m{NNNN}_{name}` naming convention.

The migration should:
1. Add a `search_vector` column of type `tsvector` to each target table (sbom, advisory, package)
2. Create GIN indexes on those columns: `CREATE INDEX idx_{table}_search ON {table} USING GIN(search_vector)`
3. Create trigger functions to auto-populate `search_vector` on row changes using `to_tsvector('english', coalesce(col1, '') || ' ' || coalesce(col2, ''))`
4. Backfill existing rows with `UPDATE {table} SET search_vector = to_tsvector(...)`

Per Key Conventions (Framework): Use SeaORM migration traits for defining the migration up/down methods. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's migration file scope.

Per Key Conventions (Error handling): All migration steps should return `Result<T, AppError>` with `.context()` wrapping for meaningful error messages on failure. Applies: task creates `migration/src/m0002_search_indexes/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] Migration adds tsvector columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on all tsvector columns
- [ ] Triggers auto-update tsvector on INSERT and UPDATE
- [ ] Existing rows are backfilled with search vectors
- [ ] Migration is reversible (down migration drops indexes, triggers, and columns)
- [ ] Migration is registered in `migration/src/lib.rs`

## Test Requirements
- [ ] Migration applies cleanly on a fresh database
- [ ] Migration rolls back cleanly (down migration)
- [ ] Inserting a new row auto-populates the search_vector column
- [ ] Updating a row refreshes the search_vector column

## Dependencies
- Depends on: None — this is the first task in the chain

[sdlc-workflow] Description digest: sha256-md:0123164515a2ed90643f13b0a7428510c25302500cbd1c77fd59d4d22cace74d
