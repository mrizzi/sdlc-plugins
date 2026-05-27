## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to optimize queries that filter by `deleted_at IS NULL`. The `list_sboms` endpoint now filters soft-deleted records by default using `query = query.filter(sbom::Column::DeletedAt.is_null())`, and this query pattern will be executed on every list request. A partial index on `deleted_at WHERE deleted_at IS NULL` will significantly improve query performance as the number of soft-deleted records grows.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` — add index creation after the column addition in the `up` method, and drop the index before column removal in the `down` method

## Implementation Notes
- Add a partial index using SeaORM migration API or raw SQL:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` migration, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- Follow existing index creation patterns in other migration files (e.g., `Index::create().name("idx_sbom_not_deleted").table(Sbom::Table)...`)

## Acceptance Criteria
- [ ] A partial index `idx_sbom_not_deleted` is created on `sbom.deleted_at WHERE deleted_at IS NULL`
- [ ] The `down` migration drops the index before removing the column
- [ ] Existing tests continue to pass with the index in place

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Review comment #30002 by reviewer-a on `migration/src/m0042_sbom_soft_delete/mod.rs` line 14:

"The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"
