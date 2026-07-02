# Review Comment Classification: Comment 30004

## Comment

**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs (line 1)
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: QUESTION

## Reasoning

The reviewer's language is interrogative, seeking clarification about a design decision:

1. **"Have you considered"** -- this is a question opener asking whether the author thought about a specific scenario. It does not assert that the behavior is wrong; it asks whether the author is aware of it.

2. **"Is that intentional?"** -- the comment ends with a direct question about intent. The reviewer is not stating that the behavior must change; they are asking whether the current behavior is by design. If the author responds "yes, that's intentional," the comment is resolved without any code change.

3. **No directive language** -- the comment does not contain phrases like "should", "must", "needs to", "please change", "fix this", or "wrap this in". It purely asks questions.

4. **Observation + question pattern** -- the reviewer observes a behavior ("direct GET still returns deleted SBOMs") and then asks whether it was intentional. This is a classic question pattern -- identifying a potentially surprising behavior and asking for confirmation.

5. **Design ambiguity** -- the task description does say `get.rs` should be modified to add `include_deleted` parameter support, which suggests the current behavior (returning deleted SBOMs via direct GET without filtering) may not be intended. However, the reviewer is asking about intent, not demanding a change. The Scope Containment check separately flags get.rs as an unimplemented file.

## Action

No sub-task created. Questions ask for clarification and do not require code changes. The related Scope Containment finding (get.rs not modified per the task spec) is tracked separately in the verification report.
