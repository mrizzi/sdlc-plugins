## Verification Report for TC-9102 (PR #743)

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments exist on the PR |
| Root-Cause Investigation | N/A | No sub-tasks created; nothing to investigate |
| Scope Containment | FAIL | 1 task-required file missing from the PR: `tests/api/advisory_summary.rs` (listed under Files to Create) |
| Diff Size | PASS | ~30 lines added across 2 files; proportionate to the implemented scope (though incomplete due to missing test file) |
| Commit Traceability | WARN | No commit metadata available in provided inputs to verify TC-9102 references |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria met; 3 criteria failed (see details below) |
| Test Quality | N/A | No test files in the PR diff. Eval Quality: N/A |
| Test Change Classification | N/A | No test files in the PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: FAIL

This PR fails verification due to critical gaps in acceptance criteria coverage and missing required files.

---

### Detailed Findings

#### Scope Containment -- FAIL

The task specifies the following files:

**Files to Modify:**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- present in diff
- `modules/fundamental/src/advisory/service/advisory.rs` -- present in diff (minimal change)

**Files to Create:**
- `tests/api/advisory_summary.rs` -- **MISSING from the diff**

The test file `tests/api/advisory_summary.rs` is listed under "Files to Create" in the task description but is entirely absent from the PR diff. The task also specifies 6 test requirements that depend on this file existing. This is a hard scope failure -- a task-required file was not created.

#### Acceptance Criteria -- FAIL (3 of 6 met)

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | `threshold=high` returns counts for critical and high only | FAIL | Filtering logic is inverted: `threshold_idx <= N` should be `N <= threshold_idx`. For threshold=high (idx=1), medium (1<=2=true) and low (1<=3=true) are wrongly included. Additionally, `total` is computed from unfiltered values. |
| 2 | Without threshold returns all severity counts (backward compatible) | PASS | The `None => summary` branch returns the unfiltered summary unchanged. |
| 3 | `threshold=invalid` returns 400 Bad Request | FAIL | Invalid values are silently accepted via `.unwrap_or(0)`, defaulting to index 0 (critical) instead of returning 400. The `AppError` type from `common/src/error.rs` exists but is not used for validation. |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | The `severity_order` array `["critical", "high", "medium", "low"]` defines the correct descending order. |
| 5 | Response includes `threshold_applied` boolean field | FAIL | The field is completely absent. The `AdvisorySummary` struct construction includes only `critical`, `high`, `medium`, `low`, and `total`. Neither the filtering branch nor the pass-through branch sets a `threshold_applied` value. |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | The SBOM fetch and error handling code is unchanged; existing 404 behavior is preserved. |

**Criterion 1 detail:** The comparison `threshold_idx <= 1` (for high), `threshold_idx <= 2` (for medium), `threshold_idx <= 3` (for low) is backwards. When threshold=high (idx=1), the condition `1 <= 2` and `1 <= 3` are both true, so medium and low are included when they should be excluded. The correct condition would check whether each field's severity index is at or above the threshold index (e.g., `1 <= threshold_idx` for high, `2 <= threshold_idx` for medium).

**Criterion 3 detail:** In `get.rs` line 45, `.unwrap_or(0)` silently converts any unrecognized threshold string to index 0 (critical). The Implementation Notes explicitly state to "Reuse `common/src/error.rs::AppError` for validation errors (return 400 for invalid threshold values)." The correct approach would use `.ok_or_else(|| AppError::BadRequest(...))` with the `?` operator.

**Criterion 5 detail:** The `threshold_applied` boolean is not present in the `AdvisorySummary` struct construction. The model struct in `modules/fundamental/src/advisory/model/summary.rs` would need a new field, and both the `Some` and `None` match arms would need to set it to `true` and `false` respectively.

#### Missing Test File

The task requires creating `tests/api/advisory_summary.rs` with 6 integration tests:
1. Test threshold=critical returns only critical count
2. Test threshold=high returns critical and high counts
3. Test threshold=medium returns critical, high, and medium counts
4. Test no threshold returns all four severity counts
5. Test invalid threshold value returns 400
6. Test non-existent SBOM ID returns 404

None of these tests exist in the PR diff. The test file was not created at all.

#### CI Status -- PASS

All CI checks pass.

#### Sensitive Patterns -- PASS

No secrets, credentials, API keys, or other sensitive patterns detected in the added lines. The diff contains only Rust application code (imports, struct definitions, handler logic).

#### Test Quality -- N/A

No test files are present in the PR diff. Repetitive Test Detection: N/A. Test Documentation: N/A. Eval Quality: N/A.

#### Test Change Classification -- N/A

No test files are present in the PR diff. Classification cannot be performed.

#### Verification Commands -- N/A

No verification commands were specified in the task description.

---

### Summary of Issues Requiring Action

1. **Missing test file:** `tests/api/advisory_summary.rs` must be created with integration tests covering all 6 test requirements from the task.

2. **Invalid threshold validation:** Replace `.unwrap_or(0)` with proper validation that returns 400 Bad Request for unrecognized threshold values, using the existing `AppError` infrastructure.

3. **Missing `threshold_applied` field:** Add a `threshold_applied: bool` field to the `AdvisorySummary` struct and set it appropriately in both the filtering and pass-through branches.

4. **Incorrect filtering logic:** The comparison direction in the threshold filtering must be fixed so that `threshold=high` correctly excludes medium and low counts.

5. **Incorrect total computation:** The `total` field should be computed from the filtered counts, not the original unfiltered values.
