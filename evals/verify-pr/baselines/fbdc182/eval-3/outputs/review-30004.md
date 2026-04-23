# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Classification:** question

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Reasoning

The reviewer asks a clarifying question about the behavior of the GET endpoint for soft-deleted SBOMs. The comment is structured as two questions ("Have you considered..." and "Is that intentional?") without prescribing a specific code change. The reviewer is seeking clarification on whether the current behavior is by design. Notably, the task description explicitly states "remains accessible via direct GET with a `?include_deleted=true` parameter," which implies the GET endpoint should support the parameter. However, the reviewer's comment is phrased as a question asking for confirmation, not as a directive to change code. No code change is explicitly requested.

## Action

No sub-task created -- this is a question seeking clarification, not a code change request.
