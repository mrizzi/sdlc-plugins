# Review Comment 30004 — Classification

**Comment by:** reviewer-a
**File:** `modules/fundamental/src/sbom/endpoints/get.rs` (line 1)
**Content:** Asks whether direct GET `/api/v2/sbom/{id}` returning soft-deleted SBOMs without `include_deleted=true` is intentional, noting that `get.rs` doesn't filter by `deleted_at`.

## Classification: code change request

## Reasoning

While the reviewer frames this as a question ("Is that intentional?"), the task description explicitly requires modifying `get.rs` to add `include_deleted` parameter support. Specifically:

1. **Task "Files to Modify" section** lists `modules/fundamental/src/sbom/endpoints/get.rs` with the note "add `include_deleted` parameter support".
2. **Task Description** states: "The SBOM is excluded from list queries but remains accessible via direct GET with a `?include_deleted=true` parameter."

The PR diff shows NO changes to `get.rs`, meaning this required file modification was not implemented. The reviewer has identified a genuine gap between the task requirements and the implementation.

This is not merely a question — it highlights a missing implementation that is explicitly required by the task's acceptance criteria. The correct behavior per the task is that `GET /api/v2/sbom/{id}` should support the `include_deleted=true` parameter, meaning by default (without the parameter) a soft-deleted SBOM should either return 404 or require the parameter to be visible. The current implementation returns deleted SBOMs unconditionally via direct GET, which contradicts the task's design.

**Initial classification:** question
**Reclassification rationale:** The question identifies a missing required implementation per the task description. This is effectively a code change request for implementing the `include_deleted` parameter in `get.rs`.
**Final classification:** code change request

**Action:** Sub-task created to add `include_deleted` parameter support to the GET /api/v2/sbom/{id} endpoint.
