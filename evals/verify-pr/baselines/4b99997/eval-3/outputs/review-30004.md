# Review Comment Classification: #30004

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Date:** 2026-04-20T14:40:00Z

## Original Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer asks for clarification about the design intent of the GET endpoint behavior with respect to soft-deleted SBOMs. The key phrases are "Have you considered" and "Is that intentional?" -- both are interrogative and seek understanding rather than demanding a change.

Looking at the task description, the acceptance criteria states:
- "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs"
- The `get.rs` file is listed under "Files to Modify" with the note "add `include_deleted` parameter support"

The task description does specify that `get.rs` should support `include_deleted`, and the diff does not show changes to `get.rs` for the GET-by-ID endpoint. However, the reviewer is raising this as a question rather than asserting it must be changed. The task description says the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter" -- this could be interpreted as the direct GET always returns the SBOM (current behavior) but the parameter adds explicit opt-in semantics.

The reviewer is asking for clarification about design intent, not requesting a code change. This is a valid question that the PR author should address in the review thread.

**Classification:** question -- no sub-task created.
