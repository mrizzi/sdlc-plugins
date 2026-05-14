# Sub-Task for Review Comment 30002

**Parent:** TC-9103
**Summary:** Add partial index on deleted_at column in SBOM soft-delete migration
**Labels:** ai-generated-jira, review-feedback

---

## Repository
trustify-backend

## Target Branch
main

## Description
The migration `m0042_sbom_soft_delete` adds a `deleted_at` column to the `sbom` table but does not create an index for it. The list endpoint filters by `deleted_at IS NULL` on every query, and without an index this filter requires a full table scan. Add a partial index on the `deleted_at` column where `deleted_at IS NULL` to optimize the frequent list query pattern.

## Files to Modify
- `migration/src/m0042_sbom_soft_delete/mod.rs` -- add a partial index creation in the `up` method and a corresponding index drop in the `down` method

## Implementation Notes
- Add the index after the `alter_table` call in the `up` method using SeaORM migration's index creation API
- The index should be a partial index filtering on `deleted_at IS NULL` for optimal performance
- SQL equivalent: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`
- In SeaORM migration, use `Index::create().name("idx_sbom_not_deleted").table(Sbom::Table).col(Sbom::DeletedAt)` with the appropriate partial index configuration
- In the `down` method, drop the index before dropping the column: `Index::drop().name("idx_sbom_not_deleted").table(Sbom::Table)`
- Check existing migration files in `migration/src/` for index creation patterns used in the project

## Acceptance Criteria
- [ ] A partial index `idx_sbom_not_deleted` is created on `sbom.deleted_at` where `deleted_at IS NULL`
- [ ] The `down` migration drops the index before dropping the column
- [ ] Existing tests continue to pass

## Test Requirements
- [ ] Existing integration tests in `tests/api/sbom_delete.rs` pass without modification
- [ ] Migration can be applied and rolled back cleanly

## Target PR
https://github.com/trustify/trustify-backend/pull/744

## Review Context
**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Comment:**
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```
