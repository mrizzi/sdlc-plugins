# Task 1: Add full-text search indexes via database migration

## Repository

trustify-backend

## Target Branch

`main`

## Description

Create a new SeaORM database migration that adds PostgreSQL full-text search infrastructure to the searchable entity tables. This includes adding `tsvector` generated columns and GIN indexes on SBOM (name, description), advisory (title, description), and package (name) tables. These indexes are the foundation for relevance-ranked full-text search in subsequent tasks.

## Files to Create

- `migration/src/m0002_search_indexes/mod.rs` -- Migration that:
  - Adds a `search_vector` column of type `tsvector` to the `sbom`, `advisory`, and `package` tables, populated via a generated column expression (e.g., `to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, ''))`)
  - Creates GIN indexes on each `search_vector` column
  - Uses `IF NOT EXISTS` guards for idempotency
  - Implements `MigrationTrait` with both `up()` and `down()` methods

## Files to Modify

- `migration/src/lib.rs` -- Register `m0002_search_indexes` in the `Migrator` struct's migration list so SeaORM discovers and runs it

## Implementation Notes

- Follow the existing migration pattern in `migration/src/`. Each migration is a module implementing `MigrationTrait` with `up` and `down` methods.
- Use raw SQL via `manager.get_connection().execute_unprepared()` for the `tsvector` column and GIN index creation, since SeaORM's schema builder does not natively support these PostgreSQL-specific types.
- For the generated column expression, use `to_tsvector('english', ...)` with `coalesce()` to handle NULL fields gracefully.
- The `down()` method should drop the GIN indexes and then drop the `search_vector` columns.
- For the advisory table, combine `title` and `description` into the tsvector. For SBOM, combine `name` and `description`. For package, use `name` alone (or `name` and `namespace` if available).
- Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to confirm exact column names before writing the migration.

## Acceptance Criteria

- [ ] Migration runs successfully against a clean PostgreSQL database
- [ ] Migration runs successfully against an existing database (idempotent guards)
- [ ] Each searchable table has a `search_vector` column of type `tsvector`
- [ ] Each `search_vector` column has a GIN index
- [ ] The `down()` migration cleanly reverses all changes
- [ ] Migration is registered and discovered by the SeaORM migrator

## Test Requirements

- Run the migration forward and backward against a test PostgreSQL instance to confirm both directions work
- Verify the indexes exist after migration using `\d+ table_name` or equivalent query
- Confirm that inserting a row into each table auto-populates the `search_vector` column

## Verification Commands

```bash
# Run migrations
cargo run --bin migration -- up

# Verify indexes exist
psql -d trustify -c "\di *search*"

# Verify tsvector columns
psql -d trustify -c "\d sbom" | grep search_vector
psql -d trustify -c "\d advisory" | grep search_vector
psql -d trustify -c "\d package" | grep search_vector

# Rollback
cargo run --bin migration -- down -n 1
```
