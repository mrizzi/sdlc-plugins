# Review Comment Classification: 30004

**Comment ID:** 30004
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** question

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification Reasoning

This is a **question**. The reviewer asks a clarifying question ("Have you considered...? Is that intentional?") about the behavior of the GET endpoint for soft-deleted SBOMs. The reviewer observes that `get.rs` was not modified to filter by `deleted_at`, and asks whether this is intentional behavior.

Notably, the task description specifies that `get.rs` should be modified to "add `include_deleted` parameter support," and the acceptance criteria state that `GET /api/v2/sbom?include_deleted=true` should include soft-deleted SBOMs. The fact that `get.rs` was not modified at all represents a gap that will be captured by the acceptance criteria verification (Step 11) and scope containment check (Step 6) rather than through review comment classification.

The reviewer's question does not directly request a code change -- it asks for clarification on intent. The underlying issue (missing `get.rs` modifications) is a task implementation gap, not something surfaced solely by reviewer judgment.

## Action

No sub-task created from this classification. The underlying gap (missing `include_deleted` support in `get.rs`) is captured by the acceptance criteria verification as a FAIL for the relevant criterion.
