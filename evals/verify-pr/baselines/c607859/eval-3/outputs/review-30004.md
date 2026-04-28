# Review Comment Classification: 30004

**Comment ID:** 30004
**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Classification:** question

## Comment Text

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification Reasoning

This is a **question**. The reviewer asks for clarification about whether a specific behavior is intentional, using question-form language ("Have you considered...?", "Is that intentional?"). The reviewer is not directing a code change but rather seeking to understand the design intent.

However, this question highlights a significant gap: the task description explicitly lists `get.rs` in "Files to Modify" with the purpose of adding `include_deleted` parameter support, and the Description states the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter." The PR diff does not include any changes to `get.rs`, meaning this file was not modified despite being in the task specification. This gap is also flagged by the Intent Alignment sub-agent (Scope Containment: FAIL) and the Correctness sub-agent (Acceptance Criteria: WARN). No sub-task created from this classification (questions do not trigger sub-tasks), but the missing `get.rs` modification is tracked through the scope containment finding.
