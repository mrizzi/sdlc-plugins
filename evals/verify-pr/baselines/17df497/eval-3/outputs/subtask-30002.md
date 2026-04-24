## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to the soft-delete migration. The default list endpoint filters by `deleted_at IS NULL` on every request, making this a high-frequency query path. A partial index on rows where `deleted_at IS NULL` will significantly improve query performance as the number of soft-deleted SBOMs grows.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index creation step in the `up` method after the `ALTER TABLE` statement, and a corresponding `DROP INDEX` step in the `down` method before the `ALTER TABLE` drop column

## Implementation Notes
- Add the index using SeaORM migration's `manager.create_index(...)` API or a raw SQL statement via `manager.get_connection().execute_unprepared(...)`
- The index should be a partial index: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL`
- In the `down` method, drop the index before dropping the column: `DROP INDEX IF EXISTS idx_sbom_not_deleted`
- If using the SeaORM `Index::create()` builder, note that partial index support (WHERE clause) may require raw SQL -- check existing migrations for precedent
- The index is specifically for optimizing the filter `sbom::Column::DeletedAt.is_null()` used in `SbomService::list`

## Acceptance Criteria
- [ ] The `up` migration creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with a `WHERE deleted_at IS NULL` condition
- [ ] The `down` migration drops the index before dropping the `deleted_at` column
- [ ] The migration runs successfully against a PostgreSQL test database
- [ ] Existing tests continue to pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Reviewer **reviewer-a** commented on `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14):

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
