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

**Reasoning**: On its surface, the comment uses suggestive phrasing ("should also add", "would help", "Something like") which could place it in the suggestion category. However, after evaluating convention upgrade eligibility, this is upgraded to a code change request.

### Convention Upgrade Analysis

The suggestion qualifies for upgrade based on the following convention alignment:

1. **Database performance convention**: Adding indexes on columns used in frequent WHERE clauses is a standard and well-established database convention. The `list` endpoint -- the primary read path for SBOMs -- filters by `deleted_at IS NULL` on every default request. Omitting an index on a column used in the WHERE clause of the highest-frequency query path would be a known performance anti-pattern.

2. **Partial index specificity**: The reviewer provides an exact SQL statement including the index name (`idx_sbom_not_deleted`), column, and partial index WHERE clause. This level of specificity indicates the reviewer considers this an expected part of the migration, not an optional enhancement.

3. **Production impact**: As the number of soft-deleted SBOMs grows, every list query will perform a full table scan on the `deleted_at` column without this index. This has direct, measurable production performance implications for the primary API endpoint.

4. **Migration completeness convention**: When a migration adds a column that is immediately used in a filter condition, the index for that filter should be part of the same migration. Splitting the column addition and its index into separate migrations creates a window where production queries run unoptimized.

Given the alignment with standard database performance conventions, the production impact on the primary list endpoint, and the specificity of the reviewer's request, this is upgraded from suggestion to code change request.

**Action**: Create sub-task (subtask-30002.md)
