## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every request, and without an index this filter requires a full table scan. A partial index (`WHERE deleted_at IS NULL`) efficiently covers the common case where most SBOMs are not deleted.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in the `up` method after the column addition, and drop the index in the `down` method before the column removal

## Implementation Notes
- Add the index using SeaORM migration's `Index::create()` API, or use a raw SQL statement via `manager.get_connection().execute_unprepared()` for the partial index syntax
- The partial index SQL: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In the `down` method, drop the index before dropping the column: `DROP INDEX IF EXISTS idx_sbom_not_deleted;`
- Check existing migration files in `migration/src/` for the pattern used for index creation in this codebase (whether `Index::create()` or raw SQL is preferred)

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with the condition `WHERE deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the column
- [ ] The migration runs successfully against a test database

## Test Requirements
- [ ] Migration up/down cycle completes without errors
- [ ] Query plan for `SELECT * FROM sbom WHERE deleted_at IS NULL` uses the partial index

## Review Context
**Reviewer:** reviewer-a
**Comment ID:** 30002
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Comment:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Target PR
https://github.com/trustify/trustify-backend/pull/744
