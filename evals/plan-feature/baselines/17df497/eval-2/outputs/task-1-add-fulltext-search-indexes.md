# Task 1 — Add full-text search indexes via database migration

## Repository
trustify-backend

## Description
Create a new SeaORM database migration that adds PostgreSQL full-text search infrastructure
to the searchable entity tables. This includes adding `tsvector` columns (or using expression-based
GIN indexes) on the `sbom`, `advisory`, and `package` tables to enable efficient full-text search.
This is a prerequisite for the SearchService refactor (Task 2) — without these indexes, the
improved search queries will fall back to sequential scans.

## Files to Modify
- `migration/src/lib.rs` — Register the new migration module in the migration list

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — Migration that:
  - Adds a `search_vector` column (`tsvector`) to `sbom`, `advisory`, and `package` tables
  - Creates GIN indexes on the `search_vector` columns
  - Creates a trigger function to auto-update `search_vector` on INSERT/UPDATE
  - Populates existing rows with initial `search_vector` values

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for
  migration structure and naming conventions.
- Use PostgreSQL `to_tsvector('english', ...)` to build the search vector from relevant
  text columns:
  - `sbom` table: name, version, description fields
  - `advisory` table: title, description, severity fields
  - `package` table: name, version, license fields
- Create GIN indexes using `CREATE INDEX ... USING GIN (search_vector)` for each table.
- Use `CREATE OR REPLACE FUNCTION` for the trigger function that maintains the `search_vector`
  column on row changes.
- Per constraints §5.2: inspect the existing migration code before writing new migration code.
- Per constraints §2.1–2.3: commits must reference TC-9002, follow Conventional Commits,
  and include the `Assisted-by: Claude Code` trailer.
- Per constraints §3.1: feature branch must be named `TC-9002`.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — Follow the established migration module structure
  and SeaORM migration trait implementation pattern.

## Acceptance Criteria
- [ ] New migration module exists and is registered in `migration/src/lib.rs`
- [ ] Migration creates `search_vector` tsvector columns on `sbom`, `advisory`, and `package` tables
- [ ] GIN indexes are created on all `search_vector` columns
- [ ] Trigger functions auto-update `search_vector` on INSERT and UPDATE
- [ ] Migration is reversible (down migration drops indexes, triggers, and columns)
- [ ] Migration runs successfully against a clean PostgreSQL database

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (`cargo run --bin migration -- up`)
- [ ] Migration rolls back cleanly (`cargo run --bin migration -- down`)
- [ ] After migration, inserting a row into `sbom`/`advisory`/`package` tables populates `search_vector` automatically
- [ ] GIN indexes are present (verify via `\di` or `pg_indexes` query)

## Verification Commands
- `cargo run --bin migration -- up` — migration applies without errors
- `cargo run --bin migration -- down` — migration rolls back without errors

## Dependencies
- None (this is the foundational task)
