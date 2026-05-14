# PR Verification Report

**Task**: [TC-9103](https://redhat.atlassian.net/browse/TC-9103) -- Add SBOM deletion endpoint
**PR**: https://github.com/trustify/trustify-backend/pull/744
**Repository**: trustify-backend
**Date**: 2026-05-14

---

## Verification Summary

| Check | Result | Details |
|---|---|---|
| Scope Containment | PASS | All modified/created files are within the task's file lists |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive data detected |
| Acceptance Criteria | PASS | All 8 acceptance criteria are satisfied by the diff |
| Test Change Classification | ADDITIVE | `tests/api/sbom_delete.rs` is a new file (entirely new test coverage) |
| Review Feedback | WARN | 2 code change requests require sub-tasks; 1 nit; 1 question |
| CI Status | PASS | All CI checks pass |

---

## Scope Containment

### Files Modified (per task "Files to Modify")

| File | Task Specifies | In Diff | Status |
|---|---|---|---|
| `entity/src/sbom.rs` | Modify | Yes | PASS |
| `modules/fundamental/src/sbom/endpoints/mod.rs` | Modify | Yes | PASS |
| `modules/fundamental/src/sbom/endpoints/list.rs` | Modify | Yes | PASS |
| `modules/fundamental/src/sbom/endpoints/get.rs` | Modify | No changes in diff | NOTE (see below) |
| `modules/fundamental/src/sbom/service/sbom.rs` | Modify | Yes | PASS |

### Files Created (per task "Files to Create")

| File | Task Specifies | In Diff | Status |
|---|---|---|---|
| `migration/src/m0042_sbom_soft_delete/mod.rs` | Create | Yes (new file) | PASS |
| `tests/api/sbom_delete.rs` | Create | Yes (new file) | PASS |

### Out-of-Scope Files

No files outside the task's specified lists were modified.

### Note on `get.rs`

The task specifies modifying `modules/fundamental/src/sbom/endpoints/get.rs` to add `include_deleted` parameter support, but no changes to this file appear in the diff. Reviewer comment 30004 raises this same observation as a question. The task description states the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter", which implies `get.rs` should support this parameter. However, it is possible the current behavior (direct GET always returns the SBOM regardless of deletion status) is intentional. This requires author clarification.

---

## Sensitive Patterns

Scanned all diff hunks for:
- Hardcoded secrets, API keys, tokens, passwords
- Connection strings with credentials
- Private keys or certificates
- `.env` file contents

**Result**: No sensitive patterns detected. The diff contains only Rust source code (entity definitions, endpoint handlers, service logic, migration, and tests).

---

## Acceptance Criteria Verification

| # | Criterion | Verdict | Evidence |
|---|---|---|---|
| 1 | `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record | PASS | `soft_delete` method in `sbom.rs` sets `deleted_at` via `Expr::value(now)` on the sbom entity |
| 2 | `DELETE /api/v2/sbom/{id}` returns 204 No Content on success | PASS | `delete_sbom` handler returns `Ok(StatusCode::NO_CONTENT)` |
| 3 | `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM | PASS | Handler uses `ok_or(AppError::NotFound("SBOM not found".into()))` |
| 4 | `DELETE /api/v2/sbom/{id}` returns 409 Conflict if already deleted | PASS | Handler checks `sbom.deleted_at.is_some()` and returns `AppError::Conflict` |
| 5 | `GET /api/v2/sbom` excludes soft-deleted SBOMs by default | PASS | `list.rs` adds `.filter(sbom::Column::DeletedAt.is_null())` when `include_deleted` is false |
| 6 | `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs | PASS | `list.rs` conditionally applies the filter based on `include_deleted` parameter |
| 7 | Related `sbom_package` and `sbom_advisory` rows are cascade-updated | PASS | `soft_delete` method updates both `sbom_package` and `sbom_advisory` with matching `sbom_id` |
| 8 | Migration adds `deleted_at` column with NULL default to `sbom` table | PASS | Migration uses `.add_column(ColumnDef::new(Sbom::DeletedAt).timestamp_with_time_zone().null())` |

---

## Test Change Classification

**Classification**: ADDITIVE

`tests/api/sbom_delete.rs` is a **new file** containing 5 new integration tests:

1. `test_delete_sbom_returns_204` -- Verifies DELETE returns 204 and SBOM is excluded from list
2. `test_delete_nonexistent_sbom_returns_404` -- Verifies DELETE on non-existent SBOM returns 404
3. `test_delete_already_deleted_sbom_returns_409` -- Verifies DELETE on already-deleted SBOM returns 409
4. `test_list_sboms_include_deleted` -- Verifies `include_deleted=true` returns deleted SBOMs
5. `test_delete_sbom_cascades_to_join_tables` -- Verifies cascade update marks related join table rows

All 5 tests from the task's Test Requirements are covered. No existing tests were modified or removed.

---

## Review Feedback

### Review Summary

1 review from **reviewer-a** with state **CHANGES_REQUESTED**, containing 4 inline comments.

### Comment Classifications

| ID | File | Classification | Sub-task Created |
|---|---|---|---|
| 30001 | `modules/fundamental/src/sbom/service/sbom.rs:60` | Code Change Request | Yes (subtask-30001.md) |
| 30002 | `migration/src/m0042_sbom_soft_delete/mod.rs:14` | Code Change Request | Yes (subtask-30002.md) |
| 30003 | `modules/fundamental/src/sbom/endpoints/mod.rs:18` | Nit | No |
| 30004 | `modules/fundamental/src/sbom/endpoints/get.rs:1` | Question | No |

### Comment Details

**30001 -- Transaction wrapping (Code Change Request)**
The reviewer identifies that the `soft_delete` method's three UPDATE statements are not wrapped in a transaction. If the sbom_advisory update fails after sbom_package succeeds, the database is left in an inconsistent state. The reviewer requests wrapping in `self.db.transaction(|txn| { ... })`. A sub-task has been created to address this.

**30002 -- Partial index on `deleted_at` (Code Change Request)**
The reviewer requests adding a partial index on `sbom.deleted_at` to optimize the frequent `WHERE deleted_at IS NULL` filter used by the list endpoint. The reviewer provides exact SQL for the index. A sub-task has been created to address this.

**30003 -- Context message wording (Nit)**
The reviewer notes that `context("SBOM not found")` is misleading because `.context()` wraps the anyhow error chain, not the HTTP response. Suggests changing to `"Failed to fetch SBOM"`. This is explicitly labeled as a nit by the reviewer and does not require a sub-task.

**30004 -- GET behavior for deleted SBOMs (Question)**
The reviewer asks whether it is intentional that `GET /api/v2/sbom/{id}` does not filter by `deleted_at`, meaning direct GET still returns deleted SBOMs without requiring `include_deleted=true`. This is a question requiring author clarification, not a code change request.

---

## Sub-tasks Created

| Sub-task File | Review Comment | Summary |
|---|---|---|
| `subtask-30001.md` | 30001 | Wrap `soft_delete` UPDATE statements in a database transaction for atomicity |
| `subtask-30002.md` | 30002 | Add partial index `idx_sbom_not_deleted` on `sbom.deleted_at` to migration |

---

## CI Status

All CI checks pass. No failures or warnings reported.

---

## Verdict

**WARN** -- PR implementation satisfies all acceptance criteria and scope requirements. However, the review contains 2 code change requests (transaction wrapping, partial index) that must be addressed via the created sub-tasks before merge. The reviewer's overall review state is CHANGES_REQUESTED.
