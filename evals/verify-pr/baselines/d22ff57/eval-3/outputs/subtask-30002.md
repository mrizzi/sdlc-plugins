## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to optimize the frequent `deleted_at IS NULL` filter used by the list endpoint. Every call to `GET /api/v2/sbom` filters by `deleted_at IS NULL`, and without an index this becomes a sequential scan as the table grows. A partial index targeting NULL values provides efficient lookup for the common case.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method and index drop in the `down` method

## Implementation Notes
- Add a partial index after the `alter_table` call in the `up` method
- Use SeaORM migration's `Index::create()` API to create the index, or use a raw SQL statement if the SeaORM API does not support partial indexes natively
- The index should be equivalent to: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In the `down` method, drop the index before dropping the column
- Check existing migration files (e.g., `migration/src/m0001_initial/mod.rs`) for patterns used when creating indexes in this project

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index on `sbom.deleted_at` filtered by `WHERE deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the `deleted_at` column
- [ ] The migration runs successfully against the test database
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Migration up and down both execute without errors (verified by existing migration test infrastructure)

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Comment text:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
