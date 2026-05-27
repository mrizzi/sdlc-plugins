## Review Comment 30004 — Classification

### Comment
**Reviewer**: reviewer-a
**File**: `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text**: "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

### Classification: Question

### Reasoning
The reviewer uses interrogative language ("Have you considered", "Is that intentional?") and is seeking clarification about the design intent, not requesting a code change. The reviewer observes that `get.rs` does not filter by `deleted_at`, which means a direct GET by ID will return soft-deleted SBOMs even without `include_deleted=true`. However, looking at the task description, this is actually the specified behavior: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The task description does indicate GET should support the parameter, but the reviewer is asking whether the current behavior (returning deleted SBOMs by default on direct GET) is intentional -- this is a design clarification question, not a code change demand.

### Action
No sub-task created. Questions require a response from the PR author to clarify design intent, not a code change. The PR author should reply explaining whether the current GET behavior aligns with the intended design from the task description.
