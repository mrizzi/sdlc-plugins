# Sub-task: Add partial index on sbom.deleted_at in migration

**Parent Task**: TC-9103
**Source**: PR review comment #30002

---

## Repository
trustify-backend

## Description
The migration `m0042_sbom_soft_delete` adds a `deleted_at` column to the `sbom` table but does not create an index to support the new query pattern. The `list_sboms` endpoint now filters by `deleted_at IS NULL` on every request. Without an index, this filter requires a full table scan on the `sbom` table, which will degrade performance as the number of SBOMs grows.

Add a partial index on the `deleted_at` column that covers rows where `deleted_at IS NULL`. This directly supports the default list query path and keeps the index small since most rows will have `deleted_at IS NULL`.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- Add index creation in the `up` method and index drop in the `down` method

## Implementation Notes
- Add the index after the `alter_table` call in the `up` method
- Use a raw SQL statement via SeaORM's `manager.get_connection().execute_unprepared()` or equivalent:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- Ensure the migration remains idempotent -- the `down` method should use `IF EXISTS` to avoid errors on re-runs
- Verify the index name does not conflict with existing indexes in the schema

## Acceptance Criteria
- [ ] Migration `up` creates a partial index `idx_sbom_not_deleted` on `sbom(deleted_at)` where `deleted_at IS NULL`
- [ ] Migration `down` drops the index before dropping the column
- [ ] The index improves query performance for the default `list_sboms` filter (`deleted_at IS NULL`)
- [ ] Existing tests continue to pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
Original review comment by **reviewer-a** on `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14):

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
