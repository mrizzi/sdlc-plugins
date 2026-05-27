## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The `list_sboms` endpoint filters by `deleted_at IS NULL` on every default query (when `include_deleted` is not set to true). Without an index, this filter requires a full table scan on the `sbom` table, which will degrade in performance as the table grows. A partial index on `deleted_at WHERE deleted_at IS NULL` will optimize this common query path.

The index should be added in the existing migration file `m0042_sbom_soft_delete/mod.rs` as part of the `up` method, and dropped in the `down` method.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add index creation in `up()` and index drop in `down()`

## Implementation Notes
- Add the index creation after the `alter_table` call in the `up` method
- Use SeaORM migration's raw SQL execution or index creation API to create the partial index:
  ```sql
  CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
  ```
- In the `down` method, drop the index before dropping the column:
  ```sql
  DROP INDEX IF EXISTS idx_sbom_not_deleted;
  ```
- If using SeaORM's `manager.create_index(...)` API, note that partial indexes (WHERE clauses) may require raw SQL via `manager.get_connection().execute_unprepared(...)` depending on the SeaORM version
- The index targets the query pattern in `modules/fundamental/src/sbom/service/sbom.rs` where `list()` filters with `query = query.filter(sbom::Column::DeletedAt.is_null())`
- Ensure the `down` migration drops the index before dropping the column to avoid dependency errors

## Acceptance Criteria
- [ ] The migration `up()` creates a partial index `idx_sbom_not_deleted` on `sbom(deleted_at) WHERE deleted_at IS NULL`
- [ ] The migration `down()` drops the index before dropping the `deleted_at` column
- [ ] The migration runs successfully against a PostgreSQL test database
- [ ] Query plans for `SELECT * FROM sbom WHERE deleted_at IS NULL` show index usage

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
"The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"
