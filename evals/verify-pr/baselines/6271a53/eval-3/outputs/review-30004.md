# Review Comment Classification: 30004

## Comment
> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**File:** `modules/fundamental/src/sbom/endpoints/get.rs`
**Line:** 1
**Author:** reviewer-a

## Classification: Question

## Reasoning

The reviewer asks for clarification about the intended behavior of the GET endpoint for individual SBOMs. The language is interrogative ("Have you considered", "Is that intentional?") rather than directive. The reviewer observes a potential gap but frames it as a question seeking the author's intent, not as a request to change code.

**Classification criteria met:**
- Reviewer asks for clarification: YES ("Have you considered", "Is that intentional?")
- Interrogative language: YES (two questions posed)
- No imperative code change request: YES (no "should", "must", "add", "change" directives)
- Seeks understanding of design decision: YES

**Note:** While this question does highlight a genuine gap (the task description specifies `include_deleted` support for GET, and `get.rs` is in the "Files to Modify" list but was not changed), the reviewer's comment is framed as a question, not a code change request. The gap in scope containment is separately captured in the verification report's Scope Containment and Acceptance Criteria checks. If the author confirms this is unintentional, it would be addressed through the existing task scope rather than a new sub-task from this review comment.

## Action
No sub-task created. Questions do not trigger sub-task creation.
