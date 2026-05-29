## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The `list` endpoint filters SBOMs by `deleted_at IS NULL` on every request, and without an index this filter requires a full table scan. A partial index on `deleted_at WHERE deleted_at IS NULL` will optimize the most common query path.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method and corresponding index drop in the `down` method

## Implementation Notes
- Add the index after the `alter_table` call in the `up` method using SeaORM's `Index::create()` API or a raw SQL statement
- The recommended index is a partial index: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- If using SeaORM's `Index::create()`, note that partial indexes may require raw SQL via `manager.get_connection().execute_unprepared()`
- In the `down` method, drop the index before dropping the column: `DROP INDEX IF EXISTS idx_sbom_not_deleted;`
- Check existing migrations in `migration/src/` for established patterns around index creation (e.g., `m0001_initial/mod.rs` or other migrations that create indexes)

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with the condition `WHERE deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the `deleted_at` column
- [ ] The index improves query performance for `SELECT ... FROM sbom WHERE deleted_at IS NULL` (the default list query)
- [ ] Migration runs successfully against the test database

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Reviewer:** reviewer-a
**Comment:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"
