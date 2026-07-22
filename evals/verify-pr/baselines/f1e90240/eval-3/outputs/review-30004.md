# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Content:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout: "Have you considered...?", "Is that intentional?" These are questions seeking clarification about a design decision, not directives requesting a code change. The reviewer observes a behavioral gap (GET by ID does not filter soft-deleted SBOMs) and asks whether this is the intended behavior rather than asserting it needs to be changed.

Note: The task's "Files to Modify" section does list `modules/fundamental/src/sbom/endpoints/get.rs` with the note "add `include_deleted` parameter support", and this file is absent from the PR diff. This gap is captured separately by the Scope Containment check (FAIL -- unimplemented file), which independently identifies the missing work regardless of how this review comment is classified.

## Action

No sub-task created. This is a question seeking clarification; no direct code change is requested. The underlying gap (missing get.rs changes) is tracked via the Scope Containment finding.
