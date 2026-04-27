# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**File:** `modules/fundamental/src/sbom/endpoints/get.rs`
**Line:** 1
**Reviewer:** reviewer-a

## Classification: question

## Reasoning

The reviewer uses classic question phrasing: "Have you considered..." and "Is that intentional?" This is asking for clarification about a design decision rather than requesting a code change. The reviewer has observed that `get.rs` does not filter by `deleted_at`, and wants to understand whether this is deliberate behavior.

Notably, the task description itself states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The task description specifies that `get.rs` should add `include_deleted` parameter support, and the PR diff does not include changes to `get.rs`. However, the reviewer is asking a clarifying question, not demanding a fix. The missing `get.rs` changes are captured separately in scope containment analysis.

This is a **question** -- the reviewer asks for clarification about the intended behavior. No sub-task created.
