## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created; nothing to investigate |
| Scope Containment | FAIL | Missing required file: `tests/api/advisory_summary.rs` (task specifies 3 files, PR modifies 2) |
| Diff Size | PASS | ~30 lines added across 2 files; proportionate to implemented scope |
| Commit Traceability | N/A | No commit metadata available in fixture data |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 3 of 6 criteria met (criteria 1, 3, 5 failed) |
| Test Quality | N/A | No test files in PR diff; Eval Quality: N/A |
| Test Change Classification | N/A | No test files in PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: FAIL

This PR fails verification due to two critical categories of issues: missing acceptance criteria and incomplete scope.

---

### Scope Containment -- FAIL

**Unimplemented files (1):**
- `tests/api/advisory_summary.rs` -- the task explicitly requires creating this integration test file with 6 test cases (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold returning 400, non-existent SBOM returning 404). The file is entirely absent from the PR diff.

**Implemented files (2 of 3):**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- modified (present in diff)
- `modules/fundamental/src/advisory/service/advisory.rs` -- modified (present in diff, minimal changes)

---

### Acceptance Criteria -- FAIL (3 of 6 met)

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | `?threshold=high` returns counts for critical and high only | FAIL | Filtering conditions are inverted: for threshold=high (idx=1), the conditions `1 <= 2` and `1 <= 3` evaluate to true, so medium and low are still included. Additionally, `total` is computed from unfiltered `summary.*` values. |
| 2 | Without threshold, returns all severity counts (backward compatible) | PASS | The `None` branch returns the original `summary` unchanged. |
| 3 | `?threshold=invalid` returns 400 Bad Request | FAIL | `.unwrap_or(0)` silently maps unrecognized threshold values to index 0 (critical) instead of returning a 400 error. No `AppError::BadRequest` usage exists for threshold validation. |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | The array `["critical", "high", "medium", "low"]` correctly defines the ordering. |
| 5 | Response includes `threshold_applied` boolean field | FAIL | The `AdvisorySummary` struct is not extended with this field. The field name `threshold_applied` does not appear anywhere in the diff. |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | The `SbomService::fetch()` call and `?` error propagation are unchanged. |

---

### Detailed Findings

#### Defect 1: Invalid threshold values silently accepted

**File:** `modules/fundamental/src/advisory/endpoints/get.rs`, threshold handling block

The code uses `.unwrap_or(0)` when looking up the threshold string in the severity array. When `position()` returns `None` (invalid input), the fallback silently treats the input as "critical" (index 0). The task's Implementation Notes explicitly state to use `common/src/error.rs::AppError` for validation errors returning 400 Bad Request.

**Impact:** Any arbitrary string passed as `?threshold=...` produces a filtered response instead of an error, violating the API contract and making client-side error handling impossible.

#### Defect 2: Missing `threshold_applied` boolean field

**File:** Not present in diff (expected in `modules/fundamental/src/advisory/model/summary.rs`)

The `AdvisorySummary` struct is not modified to include a `threshold_applied: bool` field. Neither the model file nor the endpoint code includes any reference to this field. The response cannot indicate whether filtering was applied.

**Impact:** API consumers cannot distinguish between "no advisories at this severity" and "severity was filtered out by threshold".

#### Defect 3: Filtering logic produces incorrect results

**File:** `modules/fundamental/src/advisory/endpoints/get.rs`, filtering block

The conditions for including/excluding severities are inverted. The code checks `threshold_idx <= N` when it should check `N <= threshold_idx` (or equivalently `threshold_idx >= N`). This causes all severities to be included regardless of the threshold value for most inputs:

- `threshold=critical` (idx=0): includes all four severities (should include only critical)
- `threshold=high` (idx=1): includes all four severities (should include critical and high)
- `threshold=medium` (idx=2): includes critical, medium, low but excludes high (completely wrong)

Additionally, the `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low` using the original unfiltered values, so even if filtering were correct, the total would not reflect the filtered counts.

#### Defect 4: Missing test file

**File:** `tests/api/advisory_summary.rs` -- absent from diff

The task requires creating this file with integration tests covering all 6 test scenarios specified under Test Requirements. No test file is present in the PR diff, meaning zero test coverage for the new feature.

---

### Sensitive Patterns -- PASS

No secrets, credentials, API keys, private keys, or other sensitive patterns detected in the added lines across both modified files.

---

### Diff Size -- PASS

The PR modifies 2 files with approximately 30 lines added and 2 lines removed. This is proportionate to the scope of changes actually implemented (adding a query parameter and filtering logic). The diff would be expected to be larger if the missing test file and model changes were included.

---

### Test Quality -- N/A

No test files are present in the PR diff. The task required creating `tests/api/advisory_summary.rs` with 6 integration tests, but this file is entirely absent. Repetitive Test Detection: N/A. Test Documentation: N/A. Eval Quality: N/A.

---

### Test Change Classification -- N/A

No test files are present in the PR diff. The absence of the required test file is tracked under Scope Containment.

---

### Summary of Required Actions

1. **Fix threshold validation:** Replace `.unwrap_or(0)` with proper validation that returns `AppError::BadRequest` for invalid threshold values
2. **Add `threshold_applied` field:** Extend `AdvisorySummary` with a `threshold_applied: bool` field and set it appropriately in both the filtering and non-filtering code paths
3. **Fix filtering logic:** Correct the comparison conditions so that severities below the threshold are excluded (the comparison operands are swapped)
4. **Fix total computation:** Compute `total` from the filtered values, not the original unfiltered values
5. **Create test file:** Add `tests/api/advisory_summary.rs` with the 6 required integration test cases
