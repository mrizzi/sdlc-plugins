# Review Comment Classification: 30004

## Comment

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Author:** reviewer-a

## Classification: question

## Reasoning

The reviewer asks two questions: "Have you considered...?" and "Is that intentional?" This is a request for clarification about the design decision, not a directive to change code. The reviewer is seeking to understand whether the current behavior (GET by ID still returning soft-deleted SBOMs without requiring `include_deleted=true`) is intentional or an oversight.

Notably, the task description's acceptance criteria state: "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs" for the list endpoint, and the task description says the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter." However, the implementation in `get.rs` does not add the `include_deleted` parameter filtering. This could be an intentional design choice (direct GET always returns the SBOM regardless of deletion status) or an oversight.

Regardless, the reviewer's comment is phrased as a question seeking clarification, not as a request for a code change. The appropriate response is to answer the question, not to create a sub-task.

**Triggers sub-task creation:** No
