## Repository
trustify-backend

## Target Branch
TC-9103

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every request, and without an index this filter performs a full table scan. A partial index on `deleted_at WHERE deleted_at IS NULL` enables efficient lookups for the common case (non-deleted SBOMs).

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` — add index creation in the `up` method and index drop in the `down` method

## Implementation Notes
- Add the partial index after the `alter_table` call in the `up` method using SeaORM's `Index::create()` API or a raw SQL statement
- The index should be: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In the `down` method, drop the index before dropping the column: `DROP INDEX IF EXISTS idx_sbom_not_deleted;`
- Follow the existing migration pattern in `migration/src/` for index creation

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with `WHERE deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the column
- [ ] The migration runs successfully against a fresh database
- [ ] The migration is reversible (down followed by up produces the same result)

## Test Requirements
- [ ] Verify migration runs without errors in the test environment
- [ ] Verify the index exists after migration by querying the database catalog

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Reviewer:** reviewer-a
**Comment:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```
