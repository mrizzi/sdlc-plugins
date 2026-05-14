## Repository
trustify-backend

## Target Branch
main

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every request, and without an index these queries will perform full table scans as the sbom table grows. A partial index specifically targeting `WHERE deleted_at IS NULL` provides efficient lookup for the common case (non-deleted SBOMs) while keeping the index small.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` — add index creation in the `up` method and index drop in the `down` method

## Implementation Notes
- Add the partial index after the `alter_table` call in the `up` method
- Use SeaORM migration's `Index::create()` API or a raw SQL statement to create the partial index:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- The index should be created after the column is added (order matters in the migration)

## Acceptance Criteria
- [ ] Migration `up` creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with condition `WHERE deleted_at IS NULL`
- [ ] Migration `down` drops the index before dropping the `deleted_at` column
- [ ] The list endpoint query (`WHERE deleted_at IS NULL`) benefits from the index
- [ ] Migration runs successfully against a clean database and via rollback

## Test Requirements
- [ ] Verify migration applies cleanly (existing migration test infrastructure)
- [ ] Verify migration rollback works (down drops index then column)

## Review Context
**PR Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Comment:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Target PR
https://github.com/trustify/trustify-backend/pull/744
