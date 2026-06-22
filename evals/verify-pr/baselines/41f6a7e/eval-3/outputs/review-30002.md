# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
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

This comment is classified as a **suggestion** because the reviewer proposes an optimization (adding a partial index) that would improve query performance but is not strictly required for correctness. The language uses "should also add" which suggests a recommended improvement rather than identifying a bug or broken behavior.

The reviewer correctly identifies that `deleted_at IS NULL` filtering will be frequent (the list endpoint filters by this condition by default), and a partial index would avoid full table scans. However, this is a performance optimization, not a functional requirement.

**Convention upgrade analysis:** The suggestion was evaluated for upgrade to a code change request under Check 1 (Convention Upgrade) of the Style/Conventions sub-agent. No CONVENTIONS.md content was available for this repository, and the PR diff contains only the new migration file — there are no other migration files visible in the diff to establish a codebase pattern of index creation alongside column additions. Without a documented convention or a demonstrated codebase pattern, the suggestion cannot be upgraded. It remains classified as a suggestion.

## Action

No sub-task created. The suggestion is not backed by a documented convention or demonstrated codebase pattern.
