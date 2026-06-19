# Classification Reasoning for Comment 30004

## Comment
> Have you considered what happens when someone queries `/api/v2/sbom/{id}` for a soft-deleted SBOM without `include_deleted=true`? Looking at `get.rs`, it doesn't filter by `deleted_at` — so direct GET still returns deleted SBOMs. Is that intentional?

**File:** `modules/fundamental/src/sbom/endpoints/get.rs`, line 1
**Author:** reviewer-a

## Classification: question

## Reasoning

The reviewer is asking for clarification about the design intent, not requesting a code change:

1. **"Have you considered..."** — this is a question about whether the developer thought about a particular scenario, not a directive to change behavior.
2. **"Is that intentional?"** — explicitly asks whether the current behavior is by design. The reviewer does not assert that it is wrong or that it needs to change. They are seeking clarification on the design decision.
3. **No imperative language** — the comment contains no directives like "should," "must," "fix," or "change." It asks two questions and describes the current behavior without judging it.
4. **Design ambiguity** — the task description states that soft-deleted SBOMs "remain accessible via direct GET with a `?include_deleted=true` parameter," which implies the GET endpoint should respect the parameter. The reviewer's question highlights that `get.rs` was not modified, which may or may not be a gap depending on the intended design.

While the reviewer's observation points to a potential missing implementation (the task spec mentions `include_deleted` support for GET), the comment itself is framed as a question seeking clarification, not as a change request. The scope containment check separately flags `get.rs` as an unimplemented file.

## Action

No sub-task created. This is a clarification question; no code change requested. The missing `get.rs` modification is separately tracked by the Scope Containment finding.
