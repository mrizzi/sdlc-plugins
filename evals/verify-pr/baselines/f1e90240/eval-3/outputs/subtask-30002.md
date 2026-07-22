## Repository
trustify-backend

## Target Branch
main

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to optimize the frequent `WHERE deleted_at IS NULL` filter used by the list endpoint. The soft-delete feature introduces a filter on `deleted_at IS NULL` in every list query, and without an index this filter requires a full table scan. A partial index on `deleted_at WHERE deleted_at IS NULL` efficiently supports this query pattern.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method and index removal in the `down` method

## Implementation Notes
- Add the partial index creation after the `alter_table` call in the `up` method using SeaORM's `Index::create()` API
- The index should be a partial index equivalent to: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL`
- In SeaORM migrations, use `manager.create_index(Index::create().name("idx_sbom_not_deleted").table(Sbom::Table).col(Sbom::DeletedAt)...)`
- Add corresponding `manager.drop_index(Index::drop().name("idx_sbom_not_deleted")...)` in the `down` method before the `alter_table` drop column call
- Reference other migration files in `migration/src/` for the established pattern of index creation alongside column additions

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` where `deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the column
- [ ] The migration runs successfully against the test database
- [ ] The list endpoint query performance is supported by the new index

## Test Requirements
- [ ] Verify the migration applies cleanly (up and down) without errors

## Review Context
**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Comment:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Target PR
https://github.com/trustify/trustify-backend/pull/744
