# Review Comment Classification: 30004

**Comment ID:** 30004
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Comment:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

## Reasoning

The reviewer uses interrogative language throughout: "Have you considered...", "Is that intentional?" This is a clarification question, not a directive to change code. The reviewer is asking the PR author to confirm whether the current behavior (GET by ID returns soft-deleted SBOMs without requiring `include_deleted=true`) is the intended design.

Key indicators of a question classification:
1. "Have you considered..." -- asks for reflection, not action
2. "Is that intentional?" -- explicitly requests clarification about design intent
3. No directive language ("should", "must", "needs to") is present
4. No concrete fix is proposed

Note: The task description does list `get.rs` in "Files to Modify" with "add `include_deleted` parameter support", but the file has no changes in the PR diff. This is a scope gap (get.rs was supposed to be modified but wasn't), which is captured in the Scope Containment check rather than through this review comment classification. The reviewer's comment is asking about intent, not directing a change.

## Action

No sub-task created.
