# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs
**Line:** 1
**Classification:** question

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

## Classification Reasoning

This comment is classified as a **question** because the reviewer is asking for clarification about the intended behavior rather than requesting a specific code change. Key indicators:

1. The comment opens with "Have you considered" — a question seeking the author's reasoning.
2. It closes with "Is that intentional?" — explicitly asking whether the current behavior is by design.
3. The reviewer observes a behavior gap (GET by ID returns soft-deleted SBOMs) but frames it as a question rather than directing a fix.
4. The reviewer does not prescribe what the fix should be — they are asking whether the behavior is a conscious design decision or an oversight.

Note: While this question highlights a real functional gap (the task specification includes `get.rs` in Files to Modify and the acceptance criteria imply `include_deleted` support on the GET endpoint), the reviewer's language frames this as a clarification request. The gap is separately captured by the Scope Containment check (WARN — `get.rs` missing from PR) and the Acceptance Criteria check (WARN — 7 of 8 criteria met).

## Action

No sub-task created. This asks for clarification; no code change is directly requested. The underlying gap is tracked by the Scope Containment and Acceptance Criteria findings in the verification report.
