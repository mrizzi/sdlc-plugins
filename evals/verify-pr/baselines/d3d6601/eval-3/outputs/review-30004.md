# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer is asking for clarification about the design intent, not requesting a code change. Key indicators:

1. **Interrogative language** -- "Have you considered...?" and "Is that intentional?" are questions seeking explanation, not directives
2. **Asks about design intent** -- the reviewer wants to understand whether the current behavior (GET returning soft-deleted SBOMs without filtering) is deliberate
3. **No code change requested** -- the reviewer does not say "add filtering" or "fix this"; they are asking whether the current behavior matches the author's intent
4. **Task alignment** -- the Jira task description explicitly states "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter", and the task's acceptance criteria include `GET /api/v2/sbom?include_deleted=true` for list queries. The `get.rs` endpoint for direct GET was listed as needing `include_deleted` parameter support, but the described behavior in the task ("remains accessible via direct GET") is ambiguous about whether filtering should apply to direct GET. This is a legitimate clarification question.

This is classified as a **question** because the reviewer is seeking clarification about intended behavior. No code change is explicitly requested.

**Sub-task required:** No.
