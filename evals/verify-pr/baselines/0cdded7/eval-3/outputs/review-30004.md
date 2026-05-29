# Review Comment 30004 Classification

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

**Reasoning:**

The reviewer is asking for clarification about an intentional design choice, not requesting a code change. The language is exploratory: "Have you considered...", "Is that intentional?" The reviewer observes a behavior (GET endpoint returns deleted SBOMs without filtering) and asks whether this is by design.

Importantly, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This means the task does intend for the GET endpoint to support `include_deleted=true`, and the current behavior in `get.rs` (not shown in the diff, meaning it was not modified) may be intentional -- soft-deleted SBOMs are still accessible via direct GET. The task description says SBOMs are "excluded from list queries" (handled in list.rs) but does not say they should be excluded from direct GET by default.

However, the task does list `get.rs` in Files to Modify with "add `include_deleted` parameter support", which suggests that get.rs should have been modified but was not. This is a gap that the Acceptance Criteria check will flag separately.

This is classified as a question because:
1. The language is interrogative ("Have you considered...", "Is that intentional?")
2. The reviewer is seeking clarification on design intent, not prescribing a fix
3. No imperative code change is requested
