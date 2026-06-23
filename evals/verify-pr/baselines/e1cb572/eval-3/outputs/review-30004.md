# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks a question using interrogative language: "Have you considered", "Is that intentional?". The reviewer is seeking clarification about a design decision rather than requesting a code change. The comment observes that `get.rs` does not filter by `deleted_at` and asks whether this behavior is intentional.

Notably, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This means the GET endpoint returning soft-deleted SBOMs by default is the intended behavior described in the task. The reviewer is asking for confirmation of this design choice, not requesting a change.

This asks for clarification; no code change is needed. No sub-task created.
