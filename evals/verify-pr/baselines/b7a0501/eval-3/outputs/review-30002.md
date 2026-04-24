# Review Comment Classification: 30002

## Comment
**Author**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Date**: 2026-04-20T14:35:00Z

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification
**Type**: Code Change Request
**Severity**: MEDIUM
**Creates Sub-task**: YES

## Reasoning
This comment requests a concrete code change to the migration file. The reviewer identifies a performance concern: the `list` endpoint now filters by `deleted_at IS NULL` on every request, but no database index supports this query pattern. The reviewer provides specific SQL for a partial index. Although framed as a suggestion, it constitutes a code change request because it asks for a new index to be added to the migration, which requires modifying the migration source file. The performance implication of missing this index grows with data volume, making it important enough to track as a sub-task.
