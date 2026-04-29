## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The list endpoint filters by `deleted_at IS NULL` on every query, and without an index, these queries will require full table scans as the dataset grows. A partial index specifically for NULL values optimizes the most common query path.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index creation step in the `up` method and a corresponding drop in the `down` method

## Implementation Notes
- Add a partial index after the `alter_table` call in the `up` method
- Use SeaORM migration's index creation API or a raw SQL statement for the partial index:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column
- This is a performance optimization that matches database best practices for soft-delete patterns with frequent `IS NULL` filtering

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` filtering `WHERE deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the `deleted_at` column
- [ ] The migration runs successfully against a PostgreSQL test database

## Test Requirements
- [ ] Verify the migration applies and rolls back cleanly

## Review Context
**Original review comment (PR #744, comment 30002):**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14

**Convention upgrade note:** This suggestion was upgraded to a code change request. Adding indexes for columns used in frequent filter predicates is a standard database convention for performance, particularly important for soft-delete patterns where `IS NULL` filtering occurs on every list query.

## Target PR
https://github.com/trustify/trustify-backend/pull/744
