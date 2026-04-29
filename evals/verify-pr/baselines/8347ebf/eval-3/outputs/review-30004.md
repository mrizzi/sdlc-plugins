# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning
The reviewer asks a question ("Have you considered...?", "Is that intentional?") to understand the design intent rather than requesting a specific code change. The comment seeks clarification about whether the current behavior of the GET-by-ID endpoint (returning soft-deleted SBOMs without requiring `include_deleted=true`) is deliberate or an oversight. While the question implies a potential gap, the reviewer is not directing a code change -- they are asking whether the behavior is by design. The task description does specify adding `include_deleted` parameter support to `get.rs`, suggesting this may indeed be an oversight, but the reviewer's framing is interrogative rather than imperative.

Note: The task's acceptance criteria and Files to Modify section do specify that `get.rs` should support the `include_deleted` parameter. The absence of changes to `get.rs` in the PR diff is flagged separately in the Acceptance Criteria check as an unimplemented requirement.
