## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table to the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every default query, so a partial index will significantly improve query performance as the table grows. Without this index, every list query performs a full table scan on the `deleted_at` column.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index creation statement to the `up` method and a corresponding drop index to the `down` method

## Implementation Notes
- Add the index creation after the `alter_table` call in the `up` method
- Use SeaORM migration's `Index::create()` API or a raw SQL statement to create a partial index: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL`
- In the `down` method, drop the index before dropping the column
- If using SeaORM's `Index::create()`, check whether SeaORM supports partial indexes natively; if not, use `manager.get_connection().execute_unprepared()` for raw SQL
- Ensure the migration remains idempotent (the index should not already exist when running `up`)

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index on `sbom.deleted_at` for rows where `deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the column
- [ ] The migration runs successfully against a clean database
- [ ] The migration rolls back cleanly

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs, line 14
**Comment:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"
