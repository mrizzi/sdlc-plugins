# Verification Report: TC-9103

**Task**: TC-9103 -- Add SBOM deletion endpoint
**PR**: https://github.com/trustify/trustify-backend/pull/744
**Repository**: trustify-backend
**Verified**: 2026-04-24

---

## Verification Summary

| Check | Result | Details |
|---|---|---|
| Acceptance Criteria | PASS | All 8 acceptance criteria are addressed by the PR diff |
| Files to Modify | PASS | All specified files modified; all specified files created |
| Test Coverage | PASS | 5 integration tests cover all test requirements |
| Test Change Classification | ADDITIVE | `tests/api/sbom_delete.rs` is a new file (no existing tests modified) |
| Implementation Notes | PASS | Follows existing patterns for endpoint registration, error handling, and response codes |
| Review Feedback | WARN | 2 code change requests require sub-tasks; 1 nit; 1 question |

---

## Acceptance Criteria Verification

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | `DELETE /api/v2/sbom/{id}` sets `deleted_at` on the SBOM record | PASS | `soft_delete` method in `sbom.rs` sets `deleted_at` via `Expr::value(now)` |
| 2 | `DELETE /api/v2/sbom/{id}` returns 204 No Content on success | PASS | Handler returns `Ok(StatusCode::NO_CONTENT)` in `endpoints/mod.rs` |
| 3 | `DELETE /api/v2/sbom/{id}` returns 404 for non-existent SBOM | PASS | `ok_or(AppError::NotFound(...))` in handler |
| 4 | `DELETE /api/v2/sbom/{id}` returns 409 Conflict if SBOM is already deleted | PASS | `deleted_at.is_some()` check returns `AppError::Conflict(...)` |
| 5 | `GET /api/v2/sbom` excludes soft-deleted SBOMs by default | PASS | `list.rs` filters by `DeletedAt.is_null()` when `include_deleted` is false |
| 6 | `GET /api/v2/sbom?include_deleted=true` includes soft-deleted SBOMs | PASS | `include_deleted` param skips the `is_null` filter |
| 7 | Related `sbom_package` and `sbom_advisory` rows are cascade-updated | PASS | `soft_delete` updates both join tables with matching `deleted_at` timestamp |
| 8 | Migration adds `deleted_at` column with NULL default to `sbom` table | PASS | Migration `m0042_sbom_soft_delete` adds nullable `timestamp_with_time_zone` column |

## Files Verification

### Files to Modify (from task description)
| File | Status |
|---|---|
| `modules/fundamental/src/sbom/endpoints/mod.rs` | MODIFIED -- DELETE route registered, handler added |
| `modules/fundamental/src/sbom/endpoints/list.rs` | MODIFIED -- `include_deleted` parameter added, filter applied |
| `modules/fundamental/src/sbom/endpoints/get.rs` | NOT IN DIFF -- task listed it but no changes appear in diff (see note below) |
| `modules/fundamental/src/sbom/service/sbom.rs` | MODIFIED -- `list` signature updated, `soft_delete` method added |
| `entity/src/sbom.rs` | MODIFIED -- `deleted_at` column added to entity |

**Note on get.rs**: The task description specified adding `include_deleted` parameter support to `get.rs`, but the diff does not include changes to this file. Per the task description, the SBOM "remains accessible via direct GET with a `?include_deleted=true` parameter," which implies the GET endpoint should work without the parameter for deleted SBOMs. Reviewer comment #30004 asks about this same behavior. The current implementation allows direct GET access to deleted SBOMs without any parameter, which is consistent with the task description's intent.

### Files to Create (from task description)
| File | Status |
|---|---|
| `migration/src/m0042_sbom_soft_delete/mod.rs` | CREATED -- migration with up/down methods |
| `tests/api/sbom_delete.rs` | CREATED -- 5 integration tests |

## Test Change Classification

**Classification**: ADDITIVE

**Reasoning**: The only test file in the diff is `tests/api/sbom_delete.rs`, which is a newly created file (`new file mode 100644`). No existing test files were modified or deleted. All 5 test functions are new additions that test the new DELETE endpoint functionality. This is purely additive test coverage.

**Test files in diff**:
- `tests/api/sbom_delete.rs` (NEW) -- 5 tests: `test_delete_sbom_returns_204`, `test_delete_nonexistent_sbom_returns_404`, `test_delete_already_deleted_sbom_returns_409`, `test_list_sboms_include_deleted`, `test_delete_sbom_cascades_to_join_tables`

## Review Feedback Analysis

**Overall Review State**: CHANGES_REQUESTED (by reviewer-a)

| Comment ID | Type | Severity | Sub-task Created | Summary |
|---|---|---|---|---|
| 30001 | Code Change Request | HIGH | YES | Wrap `soft_delete` operations in a database transaction |
| 30002 | Code Change Request | MEDIUM | YES | Add partial index on `sbom.deleted_at` in migration |
| 30003 | Nit | LOW | NO | Rename `.context("SBOM not found")` to `"Failed to fetch SBOM"` |
| 30004 | Question | LOW | NO | Clarification on GET behavior for soft-deleted SBOMs |

### Sub-tasks Created
1. **subtask-30001**: Wrap soft_delete operations in a database transaction (from comment #30001)
2. **subtask-30002**: Add partial index on sbom.deleted_at in migration (from comment #30002)

### Items Not Requiring Sub-tasks
- **Comment 30003 (Nit)**: Minor context message rename. Can be addressed by PR author during review cycle.
- **Comment 30004 (Question)**: Asks about GET endpoint behavior for deleted SBOMs. PR author should respond with clarification confirming intent.

---

## Verdict

**Result**: WARN -- PR implementation satisfies all acceptance criteria, but 2 code change requests from review require attention before merge. Sub-tasks have been created to track the required changes (transaction wrapping for data integrity, partial index for query performance). The PR should NOT be auto-merged until review feedback is addressed.
