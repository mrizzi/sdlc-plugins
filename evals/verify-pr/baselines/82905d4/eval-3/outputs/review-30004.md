# Review Comment 30004 — Classification

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Text:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: Question

### Reasoning

The reviewer asks for clarification about the behavior of the GET-by-ID endpoint for soft-deleted SBOMs. The language is interrogative ("Have you considered", "Is that intentional?") and does not prescribe a specific code change.

However, this question highlights an important gap: the task description explicitly lists `modules/fundamental/src/sbom/endpoints/get.rs` in the "Files to Modify" section with the note "add `include_deleted` parameter support", but the PR diff contains no changes to `get.rs`. This is an implementation omission that is captured separately under the Scope Containment check (Step 6) as a missing file.

The reviewer's question is valid -- the current implementation allows direct GET to return soft-deleted SBOMs without any parameter gating, which contradicts the task's intent for `get.rs` to support `include_deleted` parameter filtering.

### Action

No sub-task created from this classification (questions do not trigger sub-tasks). The underlying issue -- the missing `get.rs` modification -- is tracked as a Scope Containment finding.
