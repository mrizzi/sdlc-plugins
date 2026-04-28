# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Classification:** suggestion

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification Reasoning

This is a **suggestion**. The reviewer proposes adding a partial index on `deleted_at` as a performance optimization. While the language uses "should", the comment is proposing an enhancement rather than flagging a correctness issue -- the code functions correctly without the index, but query performance would benefit from it.

No CONVENTIONS.md exists in the repository to check for documented index creation conventions. Without evidence of a documented or widely demonstrated codebase convention requiring indexes on filter columns, this remains classified as a suggestion. No sub-task created.

The Style/Conventions sub-agent checked for convention upgrade eligibility:
- No CONVENTIONS.md found to match against.
- Unable to inspect the broader codebase for established index creation patterns in migrations during eval mode.
- Result: Not upgraded. Classification remains **suggestion**.
