# Review Comment Classification: 30004

**Comment ID:** 30004
**Reviewer:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs (line 1)
**Classification:** question

## Reasoning

The reviewer asks "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`?" and notes that `get.rs` doesn't filter by `deleted_at`. The comment ends with "Is that intentional?" -- this is a clarifying question about design intent, not a directive to change code.

The reviewer is raising an important observation: the task description specifies that `get.rs` should be modified to support the `include_deleted` parameter, but the PR diff shows no changes to `get.rs`. However, the reviewer's phrasing is interrogative ("Have you considered?", "Is that intentional?"), which classifies it as a question rather than a code change request.

Note: This question does highlight a potential gap in the implementation -- the task's Files to Modify section lists `get.rs` for `include_deleted` parameter support, and the Acceptance Criteria include "GET /api/v2/sbom?include_deleted=true includes soft-deleted SBOMs" (which refers to the list endpoint). The get-by-ID endpoint behavior for deleted SBOMs is not explicitly covered in acceptance criteria, but the task description does mention adding `include_deleted` parameter support to `get.rs`. This gap is separately captured in the Acceptance Criteria verification (Step 11) and Scope Containment (Step 6).

**Action:** No sub-task created. This is a clarifying question that the PR author should respond to regarding design intent.
