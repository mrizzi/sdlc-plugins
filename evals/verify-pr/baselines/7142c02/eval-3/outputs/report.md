# Verification Report: PR #744 -- Add SBOM deletion endpoint

**Task**: TC-9103
**PR**: https://github.com/trustify/trustify-backend/pull/744
**Repository**: trustify-backend
**Review State**: CHANGES_REQUESTED (reviewer-a)
**CI Status**: All checks pass

---

## Verdict: FAIL -- Changes Requested by Reviewer

The PR correctly implements the core SBOM soft-delete feature and satisfies all eight acceptance criteria from the task description. However, reviewer-a has requested changes. One review comment is an actionable code change request (transaction wrapping for the `soft_delete` method), and a sub-task has been created for it. The remaining comments are a suggestion, a nit, and a question -- none of which require sub-tasks.

---

## Domain Verification Summary

| Domain | Check | Result |
|--------|-------|--------|
| Intent Alignment | Scope Containment | PASS |
| Intent Alignment | Diff Size | PASS -- proportional to feature scope |
| Intent Alignment | Commit Traceability | PASS |
| Security | Sensitive Pattern Scan | PASS -- no credentials, secrets, or .env files |
| Correctness | CI Status | PASS -- all checks pass |
| Correctness | Acceptance Criteria | PASS -- 8/8 criteria satisfied |
| Correctness | Verification Commands | N/A -- no verification commands specified in task |
| Style/Conventions | Convention Upgrade | EVALUATED -- comment 30002 not upgraded (no convention backing) |
| Style/Conventions | Repetitive Test Detection | PASS -- no repetitive test patterns |
| Style/Conventions | Test Documentation | PASS -- all tests have doc comments |
| Style/Conventions | Test Change Classification | ADDITIVE |
| Style/Conventions | Eval Quality | N/A |
| Review Feedback | Review Processing | WARN -- code change requests exist, sub-task created |

---

## Acceptance Criteria Verification

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record | PASS | `soft_delete` in `sbom.rs` uses `update_many` with `col_expr(sbom::Column::DeletedAt, Expr::value(now))` on the sbom entity |
| 2 | `DELETE /api/v2/sbom/{id}` returns 204 No Content on success | PASS | `delete_sbom` handler returns `Ok(StatusCode::NO_CONTENT)` after successful soft-delete |
| 3 | `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM | PASS | Handler uses `.ok_or(AppError::NotFound("SBOM not found".into()))` when fetch returns None |
| 4 | `DELETE /api/v2/sbom/{id}` returns 409 Conflict if SBOM is already deleted | PASS | Handler checks `sbom.deleted_at.is_some()` and returns `AppError::Conflict("SBOM is already deleted".into())` |
| 5 | `GET /api/v2/sbom` excludes soft-deleted SBOMs by default | PASS | `list` method applies `.filter(sbom::Column::DeletedAt.is_null())` when `include_deleted` is false |
| 6 | `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs | PASS | `list` method skips the `DeletedAt.is_null()` filter when `include_deleted` is true |
| 7 | Related `sbom_package` and `sbom_advisory` rows are cascade-updated | PASS | `soft_delete` updates both `sbom_package` and `sbom_advisory` rows matching `sbom_id` with the same `deleted_at` timestamp |
| 8 | Migration adds `deleted_at` column with NULL default to `sbom` table | PASS | Migration uses `ColumnDef::new(Sbom::DeletedAt).timestamp_with_time_zone().null()` |

**Result**: 8/8 acceptance criteria satisfied in the diff.

---

## Test Requirements Verification

| # | Test Requirement | Status | Evidence |
|---|-----------------|--------|----------|
| 1 | Test DELETE returns 204 and SBOM is excluded from list | PASS | `test_delete_sbom_returns_204` asserts 204 status and verifies SBOM absence from default list |
| 2 | Test DELETE on non-existent SBOM returns 404 | PASS | `test_delete_nonexistent_sbom_returns_404` sends DELETE to `/api/v2/sbom/999999` and asserts 404 |
| 3 | Test DELETE on already-deleted SBOM returns 409 | PASS | `test_delete_already_deleted_sbom_returns_409` deletes twice and asserts 409 on second attempt |
| 4 | Test GET with `include_deleted=true` returns deleted SBOMs | PASS | `test_list_sboms_include_deleted` deletes SBOM then verifies it appears with `include_deleted=true` |
| 5 | Test cascade update marks related join table rows | PASS | `test_delete_sbom_cascades_to_join_tables` seeds SBOM with relations, deletes, and asserts `deleted_at` is set on packages |

**Result**: 5/5 test requirements covered.

---

## Test Change Classification

**Classification**: ADDITIVE

All test changes are in a **new test file** (`tests/api/sbom_delete.rs`). No existing test files were modified. The file contains 5 integration tests that exercise the new DELETE endpoint and the modified list endpoint behavior with `include_deleted` support. Test coverage aligns with the test requirements in the task description.

---

## Eval Quality

**Classification**: N/A

No eval result reviews were detected. Eval quality assessment uses three criteria: (1) comment author is `github-actions[bot]`, (2) comment body contains `## Eval Results`, and (3) comment body contains `sdlc-workflow/run-evals`. All three must match for a comment to be classified as an eval result review. No comments in this PR match these criteria.

---

## File Scope Verification

### Files to Modify (per task description)

| File | Expected | Actual |
|------|----------|--------|
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register DELETE route | PASS -- route added with `delete(delete_sbom)`, handler implemented inline |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Filter out soft-deleted, add `include_deleted` param | PASS -- `include_deleted` added to `SbomListParams`, filter applied in service call |
| `modules/fundamental/src/sbom/endpoints/get.rs` | Add `include_deleted` parameter support | NOT MODIFIED -- see Observation below |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add soft-delete logic with cascade updates | PASS -- `soft_delete` method added, `list` signature updated with `include_deleted` parameter |
| `entity/src/sbom.rs` | Add `deleted_at` column to entity | PASS -- `pub deleted_at: Option<DateTimeWithTimeZone>` added to Model struct |

### Files to Create (per task description)

| File | Expected | Actual |
|------|----------|--------|
| `migration/src/m0042_sbom_soft_delete/mod.rs` | Migration adding `deleted_at` column | PASS -- migration created with `up` and `down` methods |
| `tests/api/sbom_delete.rs` | Integration tests for deletion endpoint | PASS -- 5 test functions covering all test requirements |

### Scope Observation

`modules/fundamental/src/sbom/endpoints/get.rs` was listed as a file to modify (add `include_deleted` parameter support) but is **not modified** in this PR. The reviewer (comment 30004) raised a question about this gap. The task description says the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter", implying `get.rs` should be updated. However, the current behavior -- GET-by-ID always returning the SBOM regardless of soft-delete status -- could be considered acceptable for direct lookups. This requires team clarification.

---

## Scope Containment

- **No out-of-scope files modified**: All changed files are within the task's specified scope.
- **No unrelated changes**: The diff contains only changes related to the soft-delete feature.
- **No sensitive patterns detected**: No credentials, secrets, API keys, or `.env` files in the diff.

---

## Review Comments Summary

| ID | File | Classification | Convention Upgrade | Sub-task Created |
|----|------|---------------|-------------------|-----------------|
| 30001 | `modules/fundamental/src/sbom/service/sbom.rs` | Code change request | N/A | Yes (subtask-30001.md) |
| 30002 | `migration/src/m0042_sbom_soft_delete/mod.rs` | Suggestion | Not upgraded -- no convention backing | No |
| 30003 | `modules/fundamental/src/sbom/endpoints/mod.rs` | Nit | N/A | No |
| 30004 | `modules/fundamental/src/sbom/endpoints/get.rs` | Question | N/A | No |

Detailed classification reasoning is in `review-30001.md` through `review-30004.md`.

---

## Sub-tasks Created

1. **subtask-30001.md** -- Wrap `soft_delete` operations in a database transaction to prevent inconsistent state on partial failure.

---

## Findings

### Critical
- **Transaction safety** (comment 30001): The `soft_delete` method executes three independent UPDATE statements without a transaction. A failure in any intermediate statement leaves the database in an inconsistent partially-deleted state where some related records are marked as deleted and others are not. Sub-task created.

### Suggestion (not actioned)
- **Index on `deleted_at`** (comment 30002): The reviewer suggests adding a partial index on `deleted_at` in the migration to optimize the `deleted_at IS NULL` filter used by the list endpoint. While this is a sound performance recommendation, the reviewer uses suggestive language ("should also", "would help", "Something like"), and no documented project convention in the available fixture data requires migrations to include indexes for new filterable columns. Classified as suggestion; no sub-task created.

### Observation
- **`get.rs` not modified**: The task description specifies adding `include_deleted` support to the GET-by-ID endpoint, but the PR does not modify `get.rs`. The reviewer asked about this (comment 30004). The team should clarify whether GET-by-ID should also filter soft-deleted records by default or continue returning them unconditionally.
- **Nit on context message** (comment 30003): The `.context("SBOM not found")` message is slightly misleading since it wraps a database fetch error, not a not-found condition. The actual 404 is handled by `ok_or(AppError::NotFound(...))` on the following line. Minor cosmetic improvement, no sub-task warranted.
