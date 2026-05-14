## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to the existing migration. The list endpoint filters by `deleted_at IS NULL` on every request, and without an index this becomes a sequential scan as the table grows. A partial index restricted to `WHERE deleted_at IS NULL` will cover the most common query pattern efficiently.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method and index drop in the `down` method

## Implementation Notes
- Add the index creation after the existing `alter_table` call in the `up` method
- Use SeaORM migration's raw SQL execution or the `manager.create_index()` API to create a partial index:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- If using SeaORM's `IndexCreateStatement`, note that partial indexes (WHERE clause) may require raw SQL via `manager.get_connection().execute_unprepared()`
- The list endpoint in `modules/fundamental/src/sbom/endpoints/list.rs` already filters with `.filter(sbom::Column::DeletedAt.is_null())`, which will benefit from this index

## Acceptance Criteria
- [ ] Migration `up` creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with condition `WHERE deleted_at IS NULL`
- [ ] Migration `down` drops the index before dropping the `deleted_at` column
- [ ] Migration runs successfully against a test database (up and down)
- [ ] The index is visible in the database schema after migration

## Test Requirements
- [ ] Migration up/down cycle completes without errors
- [ ] Query plan for `SELECT * FROM sbom WHERE deleted_at IS NULL` shows index usage (manual verification)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID**: 30002
**Author**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Comment text**:
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
