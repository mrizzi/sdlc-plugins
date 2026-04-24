# Review Comment Classification: 30004

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Date**: 2026-04-20T14:40:00Z

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

**Reasoning**: The reviewer is asking for clarification about the intended behavior, not requesting a change. The language is interrogative ("Have you considered", "Is that intentional?") and the reviewer is seeking to understand whether the current behavior is by design. Looking at the task description, the specification states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The task description does mention adding `include_deleted` parameter support to `get.rs`, but the current diff does not show changes to `get.rs`. However, the reviewer is framing this as a question rather than a directive -- they want confirmation of intent before suggesting a change.

This is a valid design question. The answer depends on whether the team intends GET-by-ID to always return a soft-deleted SBOM (which is arguably correct for direct lookups) or to require the `include_deleted` parameter. The PR author should respond to clarify.

**Action**: No sub-task created. This is a question requiring author/team clarification, not an actionable code change request.
