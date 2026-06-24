# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Body:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: Question

## Reasoning

The reviewer uses interrogative language throughout: "Have you considered", "Is that intentional?" These are questions seeking clarification about a design decision, not directives to change code. The reviewer is asking whether the current behavior (GET by ID returning soft-deleted SBOMs without requiring `include_deleted=true`) is intentional or an oversight.

Notably, the task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This suggests the GET endpoint should support the parameter, but the task description also says the SBOM "remains accessible via direct GET" -- which could be interpreted as the current behavior being intentional (direct GET always returns it, with the parameter being an additional filter option on the list endpoint). The reviewer is asking for clarification on this design intent, not requesting a code change.

Since this is a request for clarification with no code change directive, it is classified as a question.

## Action

No sub-task created.
