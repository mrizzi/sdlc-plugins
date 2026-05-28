# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1

## Classification: question

## Reasoning

The reviewer is asking a question about the intended behavior of the GET endpoint for soft-deleted SBOMs. The language is interrogative: "Have you considered", "Is that intentional?" The reviewer is seeking clarification on whether the current behavior (GET returning deleted SBOMs without `include_deleted=true`) is by design or an oversight.

Notably, the task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This indicates that the task specification does expect `include_deleted` support on GET. However, the reviewer's comment is phrased as a question seeking understanding, not a directive to change code. The reviewer may be checking whether the author intentionally left GET unfiltered or forgot to implement the filter.

Since the reviewer asks for clarification rather than directing a specific code change, this is classified as a question. No sub-task is created -- the author should respond to the question directly on the PR.

## Action

No sub-task created. This is a question requiring author clarification, not a code change request.
