# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Date:** 2026-04-20T14:40:00Z

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer asks a clarifying question ("Have you considered...", "Is that intentional?") about the design behavior of the GET endpoint for soft-deleted SBOMs. The language is interrogative, not directive -- the reviewer is seeking to understand whether the current behavior is by design rather than requesting a code change. Notably, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This means the GET endpoint's current behavior (returning deleted SBOMs without requiring the flag) may be intentional or may represent a gap between the task spec and implementation -- but the reviewer is asking for clarification, not demanding a change.

The reviewer does not prescribe a fix or require any specific code modification. This is a design question that should be answered by the PR author or task owner.

## Action

No sub-task created. Questions do not trigger sub-task creation -- they require a human response to clarify intent.
