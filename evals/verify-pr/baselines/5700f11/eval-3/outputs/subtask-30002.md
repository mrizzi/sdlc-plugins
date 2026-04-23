## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every default query, and without an index this filter requires a full table scan. A partial index on rows where `deleted_at IS NULL` will efficiently support the most common query path.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` — add a partial index creation statement after the `alter_table` call in the `up` method, and a corresponding `drop_index` in the `down` method

## Implementation Notes
- Add the index in the `up` method after the existing `alter_table` call that adds the `deleted_at` column
- Use SeaORM migration's `Index::create()` API or a raw SQL statement to create the partial index:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- The index must be created after the column is added (order matters within the `up` method)
- The index must be dropped before the column is dropped (order matters within the `down` method)

## Acceptance Criteria
- [ ] Migration `m0042_sbom_soft_delete` creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` filtered to `WHERE deleted_at IS NULL`
- [ ] Migration `down` method drops the index before dropping the column
- [ ] Migration runs successfully against a clean database
- [ ] Migration rollback (`down`) runs successfully

## Test Requirements
- [ ] Migration applies and rolls back cleanly (verified by running migration up and down)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Comment:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"
