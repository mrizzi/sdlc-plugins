## Repository
trustify-backend

## Target Branch
main

## Description
Add a database migration that creates PostgreSQL full-text search indexes (GIN indexes on tsvector columns) for the SBOM, advisory, and package entities. This enables efficient full-text search queries needed by subsequent search relevance improvements. The migration adds tsvector columns and corresponding GIN indexes to support `ts_rank`-based search ranking without impacting existing queries.

## Files to Modify
- `migration/src/lib.rs` — register the new migration module in the migration runner

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that adds tsvector columns and GIN indexes to sbom, advisory, and package tables

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for module structure and SeaORM migration conventions.

The migration should:
1. Add a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables.
2. Create GIN indexes on each `search_vector` column (e.g., `CREATE INDEX idx_sbom_search_vector ON sbom USING GIN (search_vector)`).
3. Populate the `search_vector` column using `to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))` or equivalent concatenation of searchable text fields for each entity.
4. Add a trigger or note that the `search_vector` column should be updated on INSERT/UPDATE — use a PostgreSQL trigger function following standard `tsvector_update_trigger` patterns.

Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to determine which text columns should feed into the tsvector.

Register the new migration in `migration/src/lib.rs` following the same pattern used for `m0001_initial`.

Per constraints (docs/constraints.md):
- Commit messages must follow Conventional Commits and reference TC-9002 (§2.1, §2.2).
- Include `--trailer="Assisted-by: Claude Code"` on all commits (§2.3).
- Keep changes scoped to the files listed (§5.1).

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration module demonstrating the SeaORM migration pattern, use as structural template
- `entity/src/sbom.rs` — SBOM entity definition showing available text columns for tsvector population
- `entity/src/advisory.rs` — Advisory entity definition showing available text columns
- `entity/src/package.rs` — Package entity definition showing available text columns

## Acceptance Criteria
- [ ] A new migration module `m0002_search_indexes` exists and is registered in `migration/src/lib.rs`
- [ ] The migration adds `search_vector` tsvector columns to sbom, advisory, and package tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] The `search_vector` columns are populated from relevant text fields of each entity
- [ ] The migration runs successfully against a PostgreSQL test database without errors
- [ ] Existing queries and endpoints remain unaffected (backward compatible)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (up migration)
- [ ] Migration rolls back cleanly (down migration drops the columns and indexes)
- [ ] After migration, `search_vector` columns are populated for existing rows
- [ ] GIN indexes exist and are usable (verify with `EXPLAIN` showing index scan on tsvector query)

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `psql -c "\d sbom"` — verify `search_vector` column exists after migration
- `psql -c "\di idx_sbom_search_vector"` — verify GIN index exists

[sdlc-workflow] Description digest: sha256:e41603adb0b0dd508095602d11e41f2bb302138d5302274ba82983e04be5b799
