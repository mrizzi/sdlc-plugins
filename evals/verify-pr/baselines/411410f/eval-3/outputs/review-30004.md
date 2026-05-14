# Review Comment Classification: 30004

**Comment ID:** 30004
**Reviewer:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Classification:** question

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification Reasoning

The reviewer asks for clarification about the design intent. The comment uses question syntax ("Have you considered", "Is that intentional?") and does not prescribe a specific code change. The reviewer observes that `get.rs` does not filter by `deleted_at` and asks whether this is deliberate or an oversight. While this may ultimately lead to a code change, the comment itself is seeking information rather than requesting a modification.

This is a **question** because:
1. The language is interrogative ("Have you considered", "Is that intentional?")
2. The reviewer is asking for clarification on design intent, not requesting a change
3. No specific code modification is prescribed
4. The answer might be "yes, it is intentional" (the task description says deleted SBOMs remain accessible via direct GET with `include_deleted=true`)

Note: The task description does say `get.rs` should be modified to add `include_deleted` parameter support, and Scope Containment analysis flagged `get.rs` as an unimplemented file. However, the reviewer's comment is phrased as a question, not a change request.

**Action:** No sub-task created.
