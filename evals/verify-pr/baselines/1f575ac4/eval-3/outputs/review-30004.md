# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Text:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: QUESTION

## Reasoning

The reviewer is asking for clarification about the design intent. The language is interrogative: "Have you considered...", "Is that intentional?" The reviewer observes a behavior (GET endpoint returns soft-deleted SBOMs) and asks whether this is a deliberate design choice rather than requesting a specific code change. This is a request for information, not a directive to modify code.

While the question raises a valid design concern (the task specification does list `modules/fundamental/src/sbom/endpoints/get.rs` as a file to modify with `include_deleted` parameter support, and the PR does not modify that file), the reviewer's comment itself is phrased as a question seeking clarification from the author, not as a code change request.

No sub-task is created for questions.
