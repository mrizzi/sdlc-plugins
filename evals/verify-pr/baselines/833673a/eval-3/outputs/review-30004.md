## Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs, line 1
**Classification:** question

### Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

### Classification Reasoning

The reviewer asks a clarifying question ("Have you considered...?" and "Is that intentional?") about the behavior of the GET endpoint for soft-deleted SBOMs. This is a question seeking understanding of a design decision, not a direct request for a code change.

While the task specification does list `get.rs` in the "Files to Modify" section with "add include_deleted parameter support," the acceptance criteria do not include a requirement for the GET single-resource endpoint to filter by `deleted_at`. The scope containment check flagged `get.rs` as an unimplemented file, but the reviewer is asking about intent rather than requesting a fix. If the PR author confirms this is intentional, no code change is needed from this comment.

### Action

No sub-task created. This asks for clarification; no code change is explicitly requested. The missing `get.rs` change is separately tracked via the scope containment finding.
