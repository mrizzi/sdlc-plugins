# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs:1
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer uses interrogative language throughout: "Have you considered", "Is that intentional?" This is clearly a question asking for clarification about a design decision, not a directive to change code. The reviewer is raising awareness of a behavioral characteristic and seeking confirmation of intent. Questions do not trigger sub-task creation -- they require the PR author to respond with an explanation.

## Action

No sub-task created. This asks for clarification; no code change is requested.
