# Classification Reasoning for Comment 30002

## Comment
> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Author:** reviewer-a

## Classification: suggestion

## Reasoning

The reviewer's language uses "should also" and "would help" which frame this as an addendum or recommendation rather than a strict requirement:

1. **"should also add"** — the word "also" indicates this is an additional improvement beyond the core task scope, not a correction of existing behavior. It proposes something supplementary.
2. **"would help"** — hedging language indicating this is a performance optimization that may or may not be necessary depending on scale, not a correctness fix.
3. **"Something like:"** — provides a possible implementation as a starting point, not a definitive instruction. The phrasing suggests the reviewer is proposing an approach rather than mandating a specific fix.

Unlike comment 30001, which identifies a concrete correctness defect (data inconsistency), this comment addresses a performance optimization. The current code is functionally correct without the index — queries will work, they may just be slower at scale. The reviewer is proposing an alternative approach (adding a partial index) but does not require it for the PR to be correct.

**Convention upgrade check:** No CONVENTIONS.md content was available to check for documented index creation patterns. No codebase pattern evidence could be established from the PR diff alone. General database best practices are not sufficient evidence for upgrading a suggestion. The suggestion remains as-is.

## Action

No sub-task created. This is an optional performance improvement that the team may choose to address separately.
