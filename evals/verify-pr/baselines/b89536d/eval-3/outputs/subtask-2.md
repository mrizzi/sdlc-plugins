## Repository
trustify-backend

## Target Branch
main

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The `GET /api/v2/sbom` list endpoint filters by `deleted_at IS NULL` on every request, and without an index this filter requires a full table scan. A partial index on `deleted_at WHERE deleted_at IS NULL` optimizes these frequent queries.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method and index drop in the `down` method

## Implementation Notes
- Add the index after the `alter_table` call in the `up` method using SeaORM's `Index::create()` API or a raw SQL statement
- The partial index should be equivalent to: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In the `down` method, drop the index before dropping the column
- Follow the existing migration patterns in the repository's `migration/src/` directory for index creation conventions

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index on `sbom.deleted_at` for rows where `deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the `deleted_at` column
- [ ] The migration runs successfully against the test database
- [ ] List endpoint queries benefit from the index (no full table scan for `deleted_at IS NULL` filter)

## Test Requirements
- [ ] Verify migration up/down cycle completes without errors

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs, line 14
**Comment:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
