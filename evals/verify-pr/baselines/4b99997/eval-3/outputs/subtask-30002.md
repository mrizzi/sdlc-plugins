## Repository
trustify-backend

## Description
Add a partial index on the `deleted_at` column of the `sbom` table in the soft-delete migration. The `list_sboms` endpoint filters by `deleted_at IS NULL` on every default list query, making this a hot query path that will degrade as the table grows. A partial index covering rows where `deleted_at IS NULL` will optimize these frequent queries without indexing the entire column.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` — add index creation in the `up` method after the `ALTER TABLE` statement, and add corresponding index drop in the `down` method before the column drop

## Implementation Notes
- Add a partial index using SeaORM migration's `Index::create()` API after the existing `alter_table` call in the `up` method
- The index should be equivalent to: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In SeaORM migrations, use `manager.create_index(Index::create().name("idx_sbom_not_deleted").table(Sbom::Table).col(Sbom::DeletedAt).and_where(Expr::col(Sbom::DeletedAt).is_null()).to_owned()).await?;`
- In the `down` method, drop the index before dropping the column: `manager.drop_index(Index::drop().name("idx_sbom_not_deleted").table(Sbom::Table).to_owned()).await?;`
- Ensure the `up` method returns the result of both operations (use `?` on each and return `Ok(())`)

## Acceptance Criteria
- [ ] The migration `up` method creates a partial index `idx_sbom_not_deleted` on `sbom.deleted_at` with a `WHERE deleted_at IS NULL` condition
- [ ] The migration `down` method drops the index before dropping the `deleted_at` column
- [ ] The index improves query performance for the default list endpoint filter (`deleted_at IS NULL`)
- [ ] Migration runs successfully in both `up` and `down` directions

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Original comment:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
