## Repository
trustify-backend

## Target Branch
main

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every default query, making this a high-frequency filter condition. A partial index on `deleted_at WHERE deleted_at IS NULL` will optimize these queries by narrowing the index to only non-deleted rows.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** commented on `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14):

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

This comment was classified as a **code change request** (upgraded from suggestion) because adding indexes on frequently-queried filter columns is a well-established database convention, and this is a performance-critical query path (every default list query filters on `deleted_at IS NULL`).

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` — add a partial index creation step in the `up` method and a corresponding index drop in the `down` method

## Implementation Notes
- Add the index creation after the `alter_table` call in the `up` method using SeaORM's index API or a raw SQL statement
- The index should be a partial index: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL`
- In the `down` method, drop the index before dropping the column: `DROP INDEX IF EXISTS idx_sbom_not_deleted`
- Follow the existing migration patterns in the `migration/src/` directory for index creation syntax with SeaORM
- If using SeaORM's `Index::create()` API, note that partial index support may require raw SQL via `manager.get_connection().execute_unprepared()`

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom(deleted_at) WHERE deleted_at IS NULL`
- [ ] The migration `down` method drops the `idx_sbom_not_deleted` index before dropping the column
- [ ] The migration runs successfully against a PostgreSQL test database
- [ ] Existing list endpoint queries benefit from the index (verified by query plan or functional test)

## Test Requirements
- [ ] Migration applies cleanly (up and down) in the test database
- [ ] Existing SBOM list and delete tests continue to pass
