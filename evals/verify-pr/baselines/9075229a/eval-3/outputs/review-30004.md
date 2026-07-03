# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout: "Have you considered" and "Is that intentional?" This is asking for clarification about the design decision, not requesting a code change. The reviewer is pointing out an observation (get.rs does not filter by `deleted_at`) and asking whether this behavior is by design. The comment does not prescribe a fix or state that the code should be changed; it seeks to understand the intent behind the current implementation. No code change is being requested.

## Action

No sub-task created.
