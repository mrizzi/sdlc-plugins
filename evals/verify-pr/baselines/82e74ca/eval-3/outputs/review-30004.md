# Review Comment Classification: #30004

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Date:** 2026-04-20T14:40:00Z

## Original Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

## Reasoning

The reviewer asks "Have you considered..." and "Is that intentional?" — this is phrased as a question seeking clarification about a design decision, not as an explicit request for a code change. The reviewer observes that `get.rs` does not filter by `deleted_at` and asks whether this is intentional behavior.

However, this question does highlight a potential gap: the task description specifies that `get.rs` should be modified to "add `include_deleted` parameter support", and `get.rs` is listed in "Files to Modify". The PR diff does not include any changes to `get.rs`. This will be captured in the Scope Containment check (Step 6) as an unimplemented file, and in the Acceptance Criteria check (Step 11) as a potentially unmet criterion.

The comment itself remains classified as a question because the reviewer is asking for clarification rather than directing a specific code change.

## Convention Check

Not applicable — questions do not trigger convention checks.

## Action

No sub-task created. This is a clarification question. The underlying gap (missing `get.rs` changes) will be flagged through Scope Containment and Acceptance Criteria checks.
