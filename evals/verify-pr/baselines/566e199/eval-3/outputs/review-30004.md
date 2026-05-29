# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks two explicit questions: "Have you considered what happens..." and "Is that intentional?" This is a request for clarification about design intent, not a directive to change code. The reviewer is asking whether the current behavior (GET by ID returning soft-deleted SBOMs without requiring `include_deleted=true`) is intentional or an oversight. Notably, the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The GET endpoint's `include_deleted` parameter support is listed in the acceptance criteria and the task describes this as the intended behavior. The reviewer is seeking confirmation of this design choice rather than requesting a code change.

## Sub-task required: No
