## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the existing soft-delete migration. The `list` endpoint now filters by `deleted_at IS NULL` on every request, and without an index this filter requires a full table scan. A partial index on `deleted_at WHERE deleted_at IS NULL` optimizes the most common query path (listing non-deleted SBOMs) while keeping the index small.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method and index removal in the `down` method

## Implementation Notes
- Add the index after the existing `alter_table` call in the `up` method
- Use SeaORM migration's `Index::create()` API or a raw SQL statement to create a partial index:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- Follow the project's established migration pattern for index creation -- check existing migrations in `migration/src/` for examples of `Index::create` usage

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` filtering for `deleted_at IS NULL`
- [ ] The migration `down` method drops the `idx_sbom_not_deleted` index
- [ ] The migration runs successfully against the database without errors
- [ ] The `list` endpoint query benefits from the new index (queries filtering by `deleted_at IS NULL` use the index)

## Test Requirements
- [ ] Migration up/down cycle completes without errors

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Comment:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
