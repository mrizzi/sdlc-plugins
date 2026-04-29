# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Comment text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer uses interrogative language ("Have you considered", "Is that intentional?") to ask for clarification about the behavior of the GET endpoint for soft-deleted SBOMs. The reviewer is asking whether the current behavior -- where `GET /api/v2/sbom/{id}` returns soft-deleted SBOMs without requiring `include_deleted=true` -- is intentional or an oversight.

However, this question also surfaces a potential acceptance criteria gap. The task description explicitly lists `get.rs` in "Files to Modify" with the note "add `include_deleted` parameter support", and the acceptance criteria state "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs" (implying the default should exclude them). The PR diff does not include any changes to `get.rs`. This gap is captured separately in the Acceptance Criteria check of the Correctness analysis, but the comment itself is classified as a question because the reviewer is seeking clarification rather than directly requesting a code change.
