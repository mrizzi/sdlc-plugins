# Review Comment Classification: Comment 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`
**Line:** 1

## Classification: question

## Reasoning

The reviewer asks two questions: "Have you considered..." and "Is that intentional?" The comment does not request a code change or propose an alternative implementation. Instead, it asks the author to clarify the design intent behind the current behavior of the GET endpoint for soft-deleted SBOMs. The task description explicitly states "remains accessible via direct GET with a `?include_deleted=true` parameter," which suggests the current behavior (returning deleted SBOMs on direct GET) may be intentional or may need the `include_deleted` filter added -- but the reviewer is asking for clarification, not directing a change.

This is a question seeking clarification about design intent. No code change is being requested. No sub-task is warranted.

## Sub-task required: No
