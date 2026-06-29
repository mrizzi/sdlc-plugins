# Review Comment Classification: 30004

**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Date**: 2026-04-20T14:40:00Z

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

**Reasoning**: The reviewer is asking for clarification about intended behavior, not requesting a code change. The language is entirely interrogative: "Have you considered" and "Is that intentional?" are both questions seeking to understand the design decision rather than directing a modification.

The task description states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." This implies `get.rs` should have been modified to add `include_deleted` parameter support, and indeed `get.rs` was listed in the task's "Files to Modify" section. However, the PR does not modify `get.rs`, and the reviewer is framing this observation as a question rather than a directive -- they want confirmation of intent before requesting a change.

The current behavior (GET-by-ID always returns the SBOM regardless of soft-delete status) could be considered acceptable for direct lookups, since a caller who has a specific SBOM ID presumably wants to see it. Alternatively, the team may decide that `get.rs` should filter by default and require `include_deleted=true` to see deleted records, consistent with the list endpoint. This is a design decision requiring author or team input.

**Action**: No sub-task created. Questions requiring author/team clarification are not actionable code change requests.
