# Review Comment Classification: 30004

## Comment

**Author**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text**: Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: QUESTION

## Reasoning

The reviewer is asking a clarifying question about the design intent, not requesting a code change. The comment:

1. **Asks whether behavior is intentional**: The core of the comment is "Is that intentional?" -- this is a question seeking the author's reasoning, not a directive to change code.
2. **Does not prescribe a fix**: Unlike comments 30001 and 30002, this comment does not tell the author what to change or how to change it. It raises a question about whether the current behavior matches the design intent.
3. **The behavior may be correct**: The task description states "The SBOM ... remains accessible via direct GET with a `?include_deleted=true` parameter", but also notes that `get.rs` should "add `include_deleted` parameter support." The diff does not show changes to `get.rs` for filtering, which could be an oversight or could be intentional (allowing direct GET to always return the SBOM regardless). This ambiguity is exactly why the reviewer frames it as a question.

Questions do not trigger sub-task creation. The PR author should respond to clarify the design intent.

## Action

No sub-task created. This is a question requiring author clarification.
