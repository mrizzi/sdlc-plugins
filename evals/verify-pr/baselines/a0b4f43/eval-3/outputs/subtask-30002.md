## Repository
trustify-backend

## Target Branch
main

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The `list` endpoint filters by `deleted_at IS NULL` on every request, and without an index this filter requires a full table scan. A partial index (`WHERE deleted_at IS NULL`) will efficiently support this common query pattern.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index creation in the `up` method and a corresponding index drop in the `down` method

## Implementation Notes
- Add the index after the `alter_table` call in the `up` method using SeaORM's `Index::create()` API
- Create a partial index equivalent to: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In SeaORM migration, use `manager.create_index(Index::create().name("idx_sbom_not_deleted").table(Sbom::Table).col(Sbom::DeletedAt).to_owned()).await?;` -- check SeaORM documentation for partial index support or use raw SQL via `manager.get_connection().execute_unprepared(...)` if the ORM does not support WHERE clauses on indexes
- Add a corresponding `manager.drop_index(Index::drop().name("idx_sbom_not_deleted").table(Sbom::Table).to_owned()).await?;` in the `down` method before the `alter_table` column drop
- This follows the pattern used in other migrations that add indexes for frequently-filtered columns

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index on `sbom.deleted_at` for rows where `deleted_at IS NULL`
- [ ] The migration `down` method drops the index before dropping the column
- [ ] The index improves query performance for `GET /api/v2/sbom` which filters by `deleted_at IS NULL`

## Test Requirements
- [ ] Migration runs successfully (up and down) without errors
- [ ] Existing tests continue to pass

## Review Context
**Original comment by reviewer-a on `migration/src/m0042_sbom_soft_delete/mod.rs` line 14:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Target PR
https://github.com/trustify/trustify-backend/pull/744
