# Review Comment Classification: Comment 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`
**Line:** 14

## Classification: code change request

## Reasoning

The reviewer requests a specific code addition: adding a partial index on the `deleted_at` column in the migration file. While the phrase "something like" introduces the SQL example, the core request is directive -- "The migration should also add an index." The reviewer provides a concrete technical rationale (frequent `deleted_at IS NULL` queries) and a specific implementation (a partial index with a WHERE clause). This is a code change request, not merely a suggestion, because the reviewer states what the migration "should" do and provides the exact index definition.

This is a performance-related code change request that adds a missing index to support the soft-delete filtering pattern introduced by this PR.

## Sub-task required: Yes

A sub-task will be created to add a partial index on `sbom.deleted_at` in the migration file `m0042_sbom_soft_delete/mod.rs`.
