# Review Comment Classification: 30002

**Comment ID:** 30002
**Reviewer:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Classification:** suggestion

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification Reasoning

This is a **suggestion**. The reviewer proposes adding a partial index on `deleted_at` for performance optimization. The language "should also add" and "would help" frames this as a recommended improvement rather than a directive fix for broken functionality. The current implementation is functionally correct without the index -- queries will still return the right results, just potentially slower at scale. The reviewer is proposing an optimization, not fixing a bug or addressing a correctness issue.

Note: This suggestion is a candidate for convention upgrade if the project's migration conventions establish a pattern of always adding indexes for columns used in frequent filter predicates. The Style/Conventions sub-agent should evaluate whether this matches an established codebase convention.
