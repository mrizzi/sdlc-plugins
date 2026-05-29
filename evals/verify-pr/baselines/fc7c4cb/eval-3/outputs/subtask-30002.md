## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to optimize the frequent `deleted_at IS NULL` filter used by the list endpoint. The `list_sboms` handler filters soft-deleted records on every invocation via `.filter(sbom::Column::DeletedAt.is_null())`, and without an index this filter requires a full table scan. A partial index on `deleted_at WHERE deleted_at IS NULL` efficiently supports this query pattern.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method and index drop in the `down` method

## Implementation Notes
- Add the index creation after the existing `alter_table` call in the `up` method
- Use SeaORM's `Index::create()` API to define the partial index, or use a raw SQL statement for the partial index since SeaORM's index builder may not directly support `WHERE` clauses for partial indexes
- The partial index SQL equivalent: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In the `down` method, drop the index before dropping the column
- This is a performance-related change that aligns with standard database conventions for soft-delete patterns

## Acceptance Criteria
- [ ] Migration `up` method creates a partial index on `sbom.deleted_at` for `WHERE deleted_at IS NULL`
- [ ] Migration `down` method drops the index before dropping the `deleted_at` column
- [ ] The index name follows a consistent naming convention (e.g., `idx_sbom_not_deleted`)
- [ ] Existing tests continue to pass without modification

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Comment text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"
