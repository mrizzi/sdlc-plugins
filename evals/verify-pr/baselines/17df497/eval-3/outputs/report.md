# Verification Report: PR #744 -- Add SBOM deletion endpoint

**Task**: TC-9103
**PR**: https://github.com/trustify/trustify-backend/pull/744
**Repository**: trustify-backend
**Review State**: CHANGES_REQUESTED (reviewer-a)
**CI Status**: All checks pass

---

## Verdict: FAIL -- Changes Requested by Reviewer

The PR implements the core SBOM soft-delete feature correctly and satisfies most acceptance criteria. However, the reviewer has requested changes (transaction wrapping and index addition) that must be addressed before the PR can be approved. Two sub-tasks have been created for the required code changes.

---

## Acceptance Criteria Verification

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record | PASS | `soft_delete` in `sbom.rs` uses `update_many` with `col_expr(sbom::Column::DeletedAt, Expr::value(now))` |
| 2 | `DELETE /api/v2/sbom/{id}` returns 204 No Content on success | PASS | `delete_sbom` handler returns `Ok(StatusCode::NO_CONTENT)` |
| 3 | `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM | PASS | Handler uses `.ok_or(AppError::NotFound("SBOM not found".into()))` |
| 4 | `DELETE /api/v2/sbom/{id}` returns 409 Conflict if SBOM is already deleted | PASS | Handler checks `sbom.deleted_at.is_some()` and returns `AppError::Conflict(...)` |
| 5 | `GET /api/v2/sbom` excludes soft-deleted SBOMs by default | PASS | `list` method applies `.filter(sbom::Column::DeletedAt.is_null())` when `include_deleted` is false |
| 6 | `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs | PASS | `list` method skips the `DeletedAt.is_null()` filter when `include_deleted` is true |
| 7 | Related `sbom_package` and `sbom_advisory` rows are cascade-updated | PASS | `soft_delete` updates `sbom_package` and `sbom_advisory` rows matching `sbom_id` with the same `deleted_at` timestamp |
| 8 | Migration adds `deleted_at` column with NULL default to `sbom` table | PASS | Migration uses `ColumnDef::new(Sbom::DeletedAt).timestamp_with_time_zone().null()` |

**Result**: 8/8 acceptance criteria satisfied in the diff.

---

## Test Requirements Verification

| # | Test Requirement | Status | Evidence |
|---|-----------------|--------|----------|
| 1 | Test DELETE returns 204 and SBOM is excluded from list | PASS | `test_delete_sbom_returns_204` asserts 204 status and verifies SBOM absence from list |
| 2 | Test DELETE on non-existent SBOM returns 404 | PASS | `test_delete_nonexistent_sbom_returns_404` sends DELETE to `/api/v2/sbom/999999` and asserts 404 |
| 3 | Test DELETE on already-deleted SBOM returns 409 | PASS | `test_delete_already_deleted_sbom_returns_409` deletes twice and asserts 409 on second attempt |
| 4 | Test GET with `include_deleted=true` returns deleted SBOMs | PASS | `test_list_sboms_include_deleted` deletes an SBOM and verifies it appears with `include_deleted=true` |
| 5 | Test cascade update marks related join table rows | PASS | `test_delete_sbom_cascades_to_join_tables` seeds SBOM with relations, deletes, and asserts `deleted_at` is set on packages |

**Result**: 5/5 test requirements covered. All tests are in `tests/api/sbom_delete.rs` (new file).

---

## File Scope Verification

### Files to Modify (per task description)

| File | Expected | Actual |
|------|----------|--------|
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Register DELETE route | PASS -- route added with `delete(delete_sbom)`, handler implemented inline |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Filter out soft-deleted, add `include_deleted` param | PASS -- `include_deleted` added to `SbomListParams`, filter applied |
| `modules/fundamental/src/sbom/endpoints/get.rs` | Add `include_deleted` parameter support | NOT MODIFIED -- see Observation below |
| `modules/fundamental/src/sbom/service/sbom.rs` | Add soft-delete logic with cascade updates | PASS -- `soft_delete` method added, `list` signature updated |
| `entity/src/sbom.rs` | Add `deleted_at` column to entity | PASS -- `pub deleted_at: Option<DateTimeWithTimeZone>` added |

### Files to Create (per task description)

| File | Expected | Actual |
|------|----------|--------|
| `migration/src/m0042_sbom_soft_delete/mod.rs` | Migration adding `deleted_at` column | PASS -- migration created with `up` and `down` methods |
| `tests/api/sbom_delete.rs` | Integration tests | PASS -- 5 test functions covering all test requirements |

### Scope Observation

`modules/fundamental/src/sbom/endpoints/get.rs` was listed as a file to modify (add `include_deleted` parameter support) but is **not modified** in this PR. The reviewer (comment 30004) raised a question about this. The task description says the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter", which implies `get.rs` should be modified. However, the current behavior (GET always returns the SBOM regardless of soft-delete status) could be considered acceptable for direct lookups. This requires team clarification.

---

## Scope Containment

- **No out-of-scope files modified**: All changed files are within the task's specified scope.
- **No unrelated changes**: The diff contains only changes related to the soft-delete feature.
- **No sensitive patterns detected**: No credentials, secrets, API keys, or `.env` files in the diff.

---

## Review Comments Summary

| ID | File | Classification | Sub-task Created |
|----|------|---------------|-----------------|
| 30001 | `modules/fundamental/src/sbom/service/sbom.rs` | Code change request -- wrap updates in transaction | Yes (subtask-30001.md) |
| 30002 | `migration/src/m0042_sbom_soft_delete/mod.rs` | Code change request (upgraded suggestion) -- add partial index | Yes (subtask-30002.md) |
| 30003 | `modules/fundamental/src/sbom/endpoints/mod.rs` | Nit -- rename context message | No |
| 30004 | `modules/fundamental/src/sbom/endpoints/get.rs` | Question -- GET behavior for deleted SBOMs | No |

Detailed classification reasoning is in `review-30001.md` through `review-30004.md`.

---

## Sub-tasks Created

1. **subtask-30001.md** -- Wrap `soft_delete` operations in a database transaction to prevent inconsistent state on partial failure.
2. **subtask-30002.md** -- Add a partial index on `sbom.deleted_at` in the migration to optimize the high-frequency `deleted_at IS NULL` filter on list queries.

---

## Test Classification

All test changes are in a **new test file** (`tests/api/sbom_delete.rs`). There are no modifications to existing test files. All 5 tests are integration tests that exercise the new DELETE endpoint and the modified list endpoint behavior. Test coverage aligns with the test requirements in the task description.

---

## Findings

### Critical
- **Transaction safety** (comment 30001): The `soft_delete` method executes three independent UPDATE statements without a transaction. A failure in any intermediate statement leaves the database in an inconsistent partially-deleted state. Sub-task created.

### Important
- **Missing index** (comment 30002): The migration adds a `deleted_at` column but does not create an index. Since every list query filters by `deleted_at IS NULL`, this will degrade list endpoint performance as data grows. Sub-task created.

### Observation
- **`get.rs` not modified**: The task description specifies adding `include_deleted` support to the GET-by-ID endpoint, but the PR does not modify `get.rs`. The reviewer asked about this (comment 30004). The team should clarify whether GET-by-ID should also filter soft-deleted records by default.
- **Nit on context message** (comment 30003): The `.context("SBOM not found")` message is slightly misleading since it wraps a fetch error, not a not-found condition. Minor cosmetic improvement, no sub-task warranted.
