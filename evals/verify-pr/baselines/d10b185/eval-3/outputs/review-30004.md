# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Date:** 2026-04-20T14:40:00Z

> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning

The reviewer asks two explicit questions ("Have you considered...?" and "Is that intentional?") and does not request a specific code change. The comment seeks clarification about whether the current behavior of the GET endpoint -- returning soft-deleted SBOMs without requiring `include_deleted=true` -- is by design or an oversight.

Importantly, the task description in TC-9103 states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The task's acceptance criteria include `include_deleted` support for the GET endpoint, and the task's Files to Modify section lists `get.rs` with "add `include_deleted` parameter support." However, the PR diff does not show changes to `get.rs` for filtering.

Despite this potential gap, the reviewer's comment is phrased as a question seeking clarification, not as a directive to change the code. The reviewer may be checking whether the omission is intentional (perhaps the design decision was changed). The appropriate response is to answer the question, not to create a sub-task from the question itself.

Note: The acceptance criteria gap related to `get.rs` would be captured separately by the Correctness sub-agent's acceptance criteria check if the criterion is found to be unmet.

## Action

No sub-task created. Questions do not trigger sub-task creation.
