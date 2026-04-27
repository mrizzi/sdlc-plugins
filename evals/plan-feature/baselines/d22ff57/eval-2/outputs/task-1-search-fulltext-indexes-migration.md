# Task 1 — Add full-text search indexes via database migration

## Repository
trustify-backend

## Description
Create a new SeaORM database migration that adds PostgreSQL full-text search infrastructure
to the searchable entity tables (`sbom`, `advisory`, `package`). This includes adding
`tsvector` columns and GIN indexes to enable efficient full-text search, as well as trigger
functions to keep the search vectors updated on row changes. This is the foundational task
for the search improvement feature — all subsequent search changes depend on these indexes
being in place.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that:
  - Adds a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables
  - Creates GIN indexes on each `search_vector` column for fast full-text lookups
  - Creates trigger functions to auto-update `search_vector` on INSERT and UPDATE operations
  - Backfills existing rows with computed `search_vector` values

## Implementation Notes
- Follow the existing migration structure in `migration/src/m0001_initial/mod.rs` for
  module layout, naming conventions, and SeaORM migration trait implementation.
- Use PostgreSQL `to_tsvector('english', ...)` to build search vectors from relevant
  text columns in each table:
  - `sbom` table: concatenate name, version, and description fields
  - `advisory` table: concatenate title, description, and severity fields
  - `package` table: concatenate name, version, and license fields
- Create GIN indexes using `CREATE INDEX ... USING GIN (search_vector)` for each table
  to enable sub-millisecond full-text lookups.
- Create trigger functions using `CREATE OR REPLACE FUNCTION` that call
  `tsvector_update_trigger()` or a custom function to maintain `search_vector` on row changes.
- Inspect entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and
  `entity/src/package.rs` to confirm the exact column names used in each table before
  constructing the `to_tsvector()` expressions.
- The migration must be reversible — the down migration should drop indexes, triggers,
  trigger functions, and the `search_vector` columns.
- Per constraints §5.2: inspect existing migration code before writing new migration code.
- Per constraints §2.1-2.3: commits must reference TC-9002, follow Conventional Commits,
  and include the `Assisted-by: Claude Code` trailer.
- Per constraints §3.1: feature branch must be named `TC-9002`.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Follow the established migration module structure,
  SeaORM migration trait implementation, and SQL execution patterns.

## Acceptance Criteria
- [ ] New migration module exists at `migration/src/m0002_search_indexes/mod.rs`
- [ ] Migration is registered in `migration/src/lib.rs`
- [ ] `search_vector` tsvector columns are added to `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Trigger functions auto-update `search_vector` on INSERT and UPDATE
- [ ] Existing rows are backfilled with computed `search_vector` values
- [ ] Migration is reversible (down migration drops all added objects)
- [ ] Migration runs successfully against a clean PostgreSQL database

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (`cargo run --bin migration -- up`)
- [ ] Migration rolls back cleanly (`cargo run --bin migration -- down`)
- [ ] After migration, inserting a row into `sbom`, `advisory`, or `package` tables automatically populates the `search_vector` column
- [ ] GIN indexes are present and usable (verify via `pg_indexes` system catalog)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors

## Dependencies
- None (this is the foundational task)
