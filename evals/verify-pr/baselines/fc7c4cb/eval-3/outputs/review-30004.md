# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: Question

## Reasoning

The reviewer asks two explicit questions: "Have you considered what happens when..." and "Is that intentional?" The comment does not request a code change or suggest a specific modification. Instead, the reviewer is seeking clarification about the design decision to allow direct GET access to soft-deleted SBOMs without the `include_deleted=true` parameter.

Notably, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This confirms that the current behavior is intentional -- the GET endpoint intentionally does not filter by `deleted_at`, making soft-deleted SBOMs accessible via direct access. The `include_deleted` parameter filtering is specified only for the list endpoint.

This is a **question**: the reviewer asks for clarification about intentional design behavior. No code change is needed.

## Action

No sub-task created. Questions are requests for clarification that do not require code changes.
