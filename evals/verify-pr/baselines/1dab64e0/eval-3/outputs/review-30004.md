# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Content:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: QUESTION

## Reasoning

The reviewer asks for clarification about the intended behavior of the GET endpoint for soft-deleted SBOMs. The language is interrogative ("Have you considered", "Is that intentional?") rather than directive. The reviewer is not requesting a code change; they are seeking to understand whether the current behavior (GET returns deleted SBOMs without filtering) is a deliberate design choice or an oversight.

This aligns with the task description, which states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The task specifies that `get.rs` should be modified to add `include_deleted` parameter support (listed under Files to Modify). The fact that `get.rs` is not modified in the PR is captured by the Scope Containment check (unimplemented file), not by this comment classification.

The reviewer's question is legitimate and highlights the gap, but the comment itself is asking for clarification rather than directing a specific code change.

## Action

No sub-task created. This asks for clarification; no code change is directly requested. The underlying gap (missing `get.rs` modifications) is separately captured by the Scope Containment check.
