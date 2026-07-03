# Review Comment Classification: 30004

## Comment

**Author:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Text:** "Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?"

## Classification: question

## Reasoning

The reviewer asks for clarification about the intended behavior of the GET-by-ID endpoint for soft-deleted SBOMs. The language is interrogative throughout: "Have you considered...?", "Is that intentional?" The reviewer is not requesting a specific code change -- they are asking whether the current behavior is by design or an oversight.

Key factors:

1. **Interrogative language:** Both sentences are questions. "Have you considered" and "Is that intentional?" seek the author's intent, not demand a change.
2. **No directive for modification:** Unlike comment 30001 which says "Wrap the three operations in...", this comment does not prescribe what should happen. The reviewer is surfacing an observation and asking for the author's perspective.
3. **Ambiguous expected behavior:** The reviewer acknowledges it could be intentional. They are not asserting this is wrong, but asking whether it has been thought through.

**Relationship to Scope Containment:** While this comment is classified as a question (based on the reviewer's language), it surfaces the same gap detected by the Scope Containment check: `modules/fundamental/src/sbom/endpoints/get.rs` is listed in the task's "Files to Modify" but does not appear in the PR diff. The Scope Containment verdict of FAIL captures this missing implementation. The question highlights the behavioral consequence of the missing changes.

**Action:** No sub-task created. The underlying gap is captured by the Scope Containment FAIL verdict in the verification report.
