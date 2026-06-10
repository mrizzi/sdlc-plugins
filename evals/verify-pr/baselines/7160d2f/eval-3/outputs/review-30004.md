# Review Comment Classification: 30004

## Comment
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/endpoints/get.rs (line 1)
**Text:** Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` -- so direct GET still returns deleted SBOMs. Is that intentional?

## Classification: question

## Reasoning
The reviewer asks a question about behavior ("Have you considered...?", "Is that intentional?") rather than requesting a specific code change. While the question raises a valid concern about the GET endpoint not filtering soft-deleted SBOMs, the reviewer frames it as a query for clarification rather than a directive. The reviewer does not assert that this is incorrect or request a fix -- they ask whether the current behavior is intentional. This is an important question that exposes a gap (the task specification requires `get.rs` to support `include_deleted`, and the file was not modified), but the comment itself is a question. The missing `get.rs` changes are captured separately by the Scope Containment check (FAIL) and Acceptance Criteria verification. No sub-task is created from this classification, but the underlying issue is addressed through the scope containment finding.
