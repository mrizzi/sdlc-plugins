## Repository
trustify-backend

## Description
Add a database migration that creates `tsvector` generated columns on the SBOM, advisory, and package tables, and builds GIN indexes on those columns. This is the foundation for the ranked full-text search introduced in Task 2. Without these indexes, full-text queries will fall back to sequential scans and performance will not improve.

**Assumptions pending clarification**:
- Target columns are `name` and `description` on each entity. If other fields should be included in the search document (e.g. CVE IDs on advisories, version strings on packages) the migration must be updated.
- PostgreSQL's built-in `tsvector`/`tsquery` support is used rather than an external search engine (e.g. Elasticsearch), consistent with the existing PostgreSQL dependency.

## Files to Modify
- `migration/src/lib.rs` — register the new migration so SeaORM applies it in order

## Files to Create
- `migration/src/m0002_search_fts_indexes/mod.rs` — migration that adds `search_vector` generated columns and GIN indexes to `sbom`, `advisory`, and `package` tables

## Implementation Notes
Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs`. SeaORM migrations implement the `MigrationTrait` with `up()` and `down()` methods; use `manager.get_connection()` to execute raw SQL for `ALTER TABLE` statements that add generated columns, since SeaORM's schema manager does not natively support PostgreSQL generated columns.

The migration should execute statements of the form:

```sql
ALTER TABLE sbom
  ADD COLUMN search_vector tsvector
    GENERATED ALWAYS AS (to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))) STORED;

CREATE INDEX sbom_search_vector_idx ON sbom USING GIN (search_vector);
```

Repeat for the `advisory` and `package` tables.

The `down()` method must drop the indexes and columns in reverse order:

```sql
DROP INDEX IF EXISTS sbom_search_vector_idx;
ALTER TABLE sbom DROP COLUMN IF EXISTS search_vector;
```

After applying the migration, the new column will be available for use in SeaORM queries via raw SQL expressions (see Task 2).

Register the migration module in `migration/src/lib.rs` by adding it to the `migrations![]` macro invocation, matching the pattern used for `m0001_initial`.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — reference for `MigrationTrait` impl structure, `up()`/`down()` method signatures, and how to execute raw SQL through the migration manager

## Acceptance Criteria
- [ ] Running `cargo run -p migration -- up` applies the migration without error against a clean PostgreSQL database
- [ ] Running `cargo run -p migration -- down` rolls back the migration without error, removing the columns and indexes
- [ ] The `sbom`, `advisory`, and `package` tables each have a `search_vector` GIN-indexed column after migration
- [ ] The migration is idempotent: applying it twice does not error (use `IF NOT EXISTS` / `IF EXISTS` guards)

## Test Requirements
- [ ] Manual verification: after applying the migration, run `\d sbom` in psql and confirm `search_vector` column and index are present
- [ ] Verify the existing integration tests in `tests/api/sbom.rs`, `tests/api/advisory.rs`, and `tests/api/search.rs` continue to pass after the migration is applied (no schema breakage)

## Verification Commands
- `cargo run -p migration -- up` — should complete with no errors
- `cargo run -p migration -- down` — should roll back cleanly
- `cargo test -p tests` — all existing tests should still pass after schema change
