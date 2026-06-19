# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:**
> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: QUESTION

## Reasoning

1. **"Have you considered"** -- this is an interrogative opening that asks for the author's perspective, not a directive to change code.
2. **"Is that intentional?"** -- this explicitly asks for clarification about whether the current behavior is a deliberate design choice or an oversight.
3. **No code change directive:** The reviewer does not instruct the author to add filtering to get.rs. Instead, the reviewer raises an observation and asks the author to confirm or explain the behavior.
4. **Design inquiry:** The question touches on a legitimate design concern (whether direct GET should return soft-deleted SBOMs), but the reviewer defers to the author's judgment rather than prescribing a fix.

Note: The task description does state that "GET /api/v2/sbom/{id}" should support `include_deleted=true`, and the `get.rs` file is listed in Files to Modify. However, the reviewer's comment is phrased as a question seeking clarification, not as a code change request. The acceptance criteria gap (if any) would be caught by the Correctness sub-agent's acceptance criteria verification, not by review comment classification.

## Action

No sub-task created. Questions request clarification and do not trigger sub-task creation.
