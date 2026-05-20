## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every request, and without an index this requires a full table scan. A partial index limited to `WHERE deleted_at IS NULL` optimizes this high-frequency query pattern.

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Original comment:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**Convention upgrade note:** This comment was upgraded from suggestion to code change request based on codebase convention analysis -- the repository uses an established migration pattern, and adding indexes for frequently-queried filter columns is a standard database convention for performance.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index creation statement in the `up` method and a corresponding drop index statement in the `down` method

## Implementation Notes
- Add the index creation after the `alter_table` call in the `up` method using SeaORM's `Index::create()` API or a raw SQL statement
- The partial index should be: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL`
- In the `down` method, add a corresponding `Index::drop()` or raw SQL `DROP INDEX idx_sbom_not_deleted` before the `alter_table` column drop
- Follow the existing migration patterns in the `migration/src/` directory for index creation syntax
- The index optimizes the filter `sbom::Column::DeletedAt.is_null()` used in `modules/fundamental/src/sbom/service/sbom.rs` list method

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with condition `WHERE deleted_at IS NULL`
- [ ] The migration `down` method drops the index before removing the column
- [ ] The migration runs successfully against a PostgreSQL test database
- [ ] The list endpoint query benefits from the index (the filter `deleted_at IS NULL` matches the partial index condition)
