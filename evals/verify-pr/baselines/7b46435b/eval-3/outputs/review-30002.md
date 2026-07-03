# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column for performance optimization. While the language uses "should also add," this is a suggestion for an enhancement beyond the task's specified requirements, not a correction of existing code.

Key factors for classifying as **suggestion** rather than code change request:

1. **Performance optimization, not correctness:** The migration works correctly without the index. Adding an index is a performance improvement -- queries will still return correct results without it, they will just be slower at scale.
2. **Not in task specification:** The task's acceptance criteria and implementation notes do not mention indexes. The reviewer is proposing an additional improvement beyond what the task requires.
3. **Suggestive phrasing:** "should also add" and "would help" indicate a recommendation, not a requirement. The word "also" implies this is an addition to the existing work, not a fix to it.

**Convention upgrade eligibility:** This suggestion was evaluated for convention upgrade by the Style/Conventions sub-agent (Check 1). CONVENTIONS.md content for the target repository was not available, and no codebase patterns demonstrating consistent index creation in migrations could be verified from the PR diff alone. Without concrete convention evidence (documented or demonstrated), the suggestion remains classified as a suggestion per the upgrade rules (general database best practices are not sufficient for upgrade).

**Action:** No sub-task created. The suggestion is noted in the verification report for the reviewer's awareness.
