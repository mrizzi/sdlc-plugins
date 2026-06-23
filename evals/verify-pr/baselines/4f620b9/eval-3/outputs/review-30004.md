## Review Comment 30004 — Classification

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Content:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

### Classification: question

### Reasoning

The reviewer asks a question ("Have you considered...?", "Is that intentional?") seeking clarification about a design decision. The comment does not request a code change or suggest an alternative — it asks the PR author whether the current behavior (GET by ID returning soft-deleted SBOMs without requiring `include_deleted=true`) is deliberate or an oversight.

This is a valid observation: the task's Files to Modify list includes `get.rs` with the note "add `include_deleted` parameter support," but the PR diff does not include changes to `get.rs`. However, the acceptance criteria as written only reference `GET /api/v2/sbom` (the list endpoint) for the `include_deleted` filter, not the individual GET endpoint. The reviewer is asking for clarification on this ambiguity. This is properly classified as a question — the PR author should respond to clarify the intent.

Note: The missing `get.rs` modification is separately flagged by the Scope Containment check as an unimplemented file (FAIL), which is a structural verification independent of this review comment.

### Action

No sub-task created.
