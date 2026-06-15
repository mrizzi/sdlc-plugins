# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs (line 1)
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: Question

## Reasoning

The reviewer is asking for clarification, not requesting a code change. The language is interrogative throughout:
- "Have you considered..." -- asking whether the author thought about this scenario
- "Is that intentional?" -- asking for confirmation of design intent

The reviewer observes that `get.rs` does not filter by `deleted_at`, meaning a direct GET on a soft-deleted SBOM still returns it. However, rather than asserting this is wrong and requesting a fix, the reviewer asks whether this behavior is by design. This is significant because the task description explicitly states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter." The current behavior (GET returning deleted SBOMs without the parameter) could be intentional or could be a gap -- the reviewer is seeking clarification rather than prescribing a change.

Questions ask for clarification and do not constitute code change requests. The PR author should respond to explain the intended behavior, but no code modification is being requested.

## Action

No sub-task created. Questions do not trigger sub-task creation.
