# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** question

## Reasoning

The reviewer asks two questions and does not direct any code change:

- "**Have you considered** what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`?" -- this is an open-ended question seeking the author's perspective on the design decision.
- "**Is that intentional?**" -- explicitly asks whether the current behavior is by design.

The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning a direct GET for a specific SBOM ID still returns soft-deleted SBOMs. Rather than directing a change, the reviewer asks whether this behavior is intentional. This is a clarification question, not a code change request.

Note: The task description explicitly states that GET should remain accessible for soft-deleted SBOMs with `?include_deleted=true`, and the `get.rs` file is listed in "Files to Modify" with the note "add `include_deleted` parameter support." However, the diff does not show changes to `get.rs` for this parameter. This gap is covered by the acceptance criteria check in the Correctness domain, not by this comment classification.

**Action:** No sub-task created.
