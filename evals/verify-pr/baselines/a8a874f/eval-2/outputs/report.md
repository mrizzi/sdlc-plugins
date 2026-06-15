## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created; nothing to investigate |
| Scope Containment | FAIL | `tests/api/advisory_summary.rs` is listed in Files to Create but absent from the diff; task-required file is missing |
| Diff Size | PASS | 2 files changed with proportionate additions (~30 lines) for the described task scope |
| Commit Traceability | N/A | No commit data available in fixture to evaluate |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass (per eval scenario) |
| Acceptance Criteria | FAIL | 3 of 6 criteria met; 3 criteria fail (invalid threshold validation, threshold_applied field, threshold filtering logic) |
| Test Quality | N/A | No test files in the PR diff. Eval Quality: N/A |
| Test Change Classification | N/A | No test files in the PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: FAIL

This PR fails verification due to multiple unmet acceptance criteria and a missing task-required file.

---

### Detailed Findings

#### Scope Containment -- FAIL

The task specifies the following files:

**Files to Modify:**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- present in diff
- `modules/fundamental/src/advisory/service/advisory.rs` -- present in diff

**Files to Create:**
- `tests/api/advisory_summary.rs` -- MISSING from diff

The test file `tests/api/advisory_summary.rs` is listed under "Files to Create" in the task description but is entirely absent from the PR diff. The task includes 6 specific test requirements (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold, non-existent SBOM) that should be covered by this file. None of these tests exist in the PR.

**Unimplemented files:** `tests/api/advisory_summary.rs`
**Out-of-scope files:** None

#### Diff Size -- PASS

The diff modifies 2 files with approximately 30 lines of additions, which is proportionate to the task scope (adding a query parameter and filtering logic to an existing endpoint). However, the expected file count is 3 (2 to modify + 1 to create), and only 2 are present due to the missing test file.

#### Sensitive Patterns -- PASS

No sensitive patterns detected in added lines. The additions consist of a struct definition, query parameter extraction, and filtering logic. No hardcoded credentials, API keys, tokens, or other secrets are present.

#### CI Status -- PASS

All CI checks pass per the eval scenario constraints.

#### Acceptance Criteria -- FAIL

3 of 6 acceptance criteria are met. Detailed per-criterion analysis:

| # | Criterion | Result | Issue |
|---|-----------|--------|-------|
| 1 | threshold=high returns critical and high only | FAIL | Filtering logic is inverted; `threshold_idx <= N` includes severities below the threshold instead of excluding them. For threshold=high, medium and low are incorrectly included. |
| 2 | No threshold returns all counts (backward compatible) | PASS | The `None => summary` arm correctly returns unfiltered results. |
| 3 | threshold=invalid returns 400 Bad Request | FAIL | `unwrap_or(0)` silently converts invalid values to index 0 (critical) instead of returning a 400 error. The `AppError` type is imported but never used for validation. |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | The `severity_order` array correctly defines `["critical", "high", "medium", "low"]`. |
| 5 | Response includes threshold_applied boolean field | FAIL | No `threshold_applied` field is added to the response. The `AdvisorySummary` model is not modified, and the field is absent from the constructed struct. |
| 6 | 404 for non-existent SBOM IDs preserved | PASS | The existing `SbomService::fetch()` call and its error propagation are unchanged. The 404 path is unaffected. |

**Critical issues:**

1. **Missing 400 validation (Criterion 3):** The code uses `unwrap_or(0)` to handle unrecognized threshold values, silently defaulting to the "critical" threshold. The task explicitly requires returning 400 Bad Request for invalid values and the Implementation Notes specify using `AppError` for validation errors. This is a silent data integrity issue -- callers with typos in the threshold value receive filtered results without any indication that their input was invalid.

2. **Missing threshold_applied field (Criterion 5):** The response struct `AdvisorySummary` is not modified to include a `threshold_applied: bool` field. Neither the model file (`modules/fundamental/src/advisory/model/summary.rs`) nor the endpoint handler adds this field. API consumers have no way to determine programmatically whether filtering was applied to the response.

3. **Inverted filtering logic (Criterion 1):** The comparison `threshold_idx <= N` is backwards. For threshold=high (idx=1), the condition `1 <= 2` evaluates to true for medium, incorrectly including it. The correct condition is `N <= threshold_idx` to include only severities at index positions up to and including the threshold position. Additionally, the `total` field is computed from unfiltered counts.

#### Test Quality -- N/A

No test files are present in the PR diff. The task requires creation of `tests/api/advisory_summary.rs` with 6 specific test cases, but this file is entirely missing. Eval Quality: N/A (no eval result reviews found).

#### Test Change Classification -- N/A

No test files are present in the PR diff to classify.

#### Verification Commands -- N/A

No verification commands were specified in the task description, and no eval infrastructure changes are present in the diff.

---

### Summary of Issues Requiring Attention

1. **Missing test file:** `tests/api/advisory_summary.rs` must be created with integration tests covering all 6 test requirements from the task.
2. **Missing input validation:** Replace `unwrap_or(0)` with proper validation that returns 400 Bad Request for invalid threshold values, using the existing `AppError` mechanism.
3. **Missing response field:** Add `threshold_applied: bool` to the `AdvisorySummary` struct and set it to `true` when a threshold is active, `false` otherwise.
4. **Inverted filtering logic:** Fix the comparison direction in the threshold filtering conditions so that only severities at or above the threshold are included.
5. **Incorrect total computation:** Compute `total` from the filtered counts, not from the original unfiltered values.
