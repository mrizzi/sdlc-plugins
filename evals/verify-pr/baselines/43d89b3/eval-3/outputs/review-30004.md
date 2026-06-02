# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Body:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning
The reviewer asks a clarifying question about the design intent: whether the GET endpoint's current behavior (returning soft-deleted SBOMs without requiring `include_deleted=true`) is intentional. The phrasing "Have you considered" and "Is that intentional?" are questions seeking clarification, not directives to change code. The reviewer has identified a potential gap but is asking the author to confirm whether this is by design. The task description does state that "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter," which implies the GET endpoint should also filter -- but the reviewer is asking rather than demanding. This is a question.
