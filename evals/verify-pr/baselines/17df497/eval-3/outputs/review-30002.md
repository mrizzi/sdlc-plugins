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

**Reasoning**: The comment is phrased as a suggestion ("should also add", "would help"), but it rises to the level of a code change request for two reasons:

1. **Convention alignment**: Adding indexes for frequently-filtered columns is a standard database performance convention. The `list` endpoint filters by `deleted_at IS NULL` on every default query, making this a high-frequency query path. Omitting an index on a column used in a WHERE clause on every list call would be a performance concern in production.

2. **Specificity**: The reviewer provides an exact SQL statement and names the index, indicating this is an expected addition rather than an optional enhancement.

Given the performance implications for the primary list endpoint and the alignment with standard database practices, this is upgraded from a suggestion to a code change request.

**Action**: Create sub-task (subtask-30002.md)
