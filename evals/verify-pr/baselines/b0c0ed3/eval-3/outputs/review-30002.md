# Review Comment Classification: 30002

**Reviewer**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Date**: 2026-04-20T14:35:00Z

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: Code Change Request (upgraded from suggestion)

**Reasoning**: The reviewer's language is phrased as a suggestion ("should also add", "would help"), which would normally classify as a suggestion. However, this is upgraded to a code change request for the following reasons:

1. **Performance impact on a primary query path**: The `list` endpoint in `modules/fundamental/src/sbom/endpoints/list.rs` applies a `.filter(sbom::Column::DeletedAt.is_null())` on every default request. This is the main SBOM listing endpoint -- one of the highest-frequency queries in the system. Without an index, this filter requires a sequential scan of the entire `sbom` table, which will degrade proportionally as the table grows.

2. **Standard database convention**: Adding indexes for columns used in frequent WHERE clause filters is a foundational database performance practice. Omitting an index on a column that is filtered on every list query is a performance defect, not merely an optional enhancement.

3. **Specificity of the request**: The reviewer provides an exact SQL statement with a named index (`idx_sbom_not_deleted`) and a partial index condition (`WHERE deleted_at IS NULL`), indicating this is an expected addition rather than an exploratory idea.

Given the direct performance implications for the primary list endpoint and the alignment with standard database indexing practices, this is upgraded from suggestion to code change request.

**Action**: Create sub-task (subtask-30002.md)
