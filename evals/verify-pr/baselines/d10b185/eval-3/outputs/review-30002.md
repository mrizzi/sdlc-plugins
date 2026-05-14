# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Date:** 2026-04-20T14:35:00Z

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: code change request

## Reasoning

The reviewer uses directive language ("should also add an index") and identifies a performance concern backed by concrete technical reasoning: the list endpoint filters by `deleted_at IS NULL` on every query, and without an index this will result in a full table scan. The reviewer provides the specific SQL for a partial index.

While this could initially appear as a suggestion (proposing an optimization), it qualifies as a code change request for two reasons:

1. **Directive language**: "should also add" is imperative, not optional ("you might consider" or "it would be nice if").
2. **Functional impact**: Without the index, the `deleted_at IS NULL` filter applied in every list query will degrade performance as the table grows. This is a missing component of the migration, not an optional enhancement.

The reviewer is identifying an omission in the migration -- the `deleted_at` column was added without the corresponding index needed to support the query pattern that uses it.

## Action

Sub-task creation required. The migration must be updated to include a partial index on the `deleted_at` column for the `sbom` table.
