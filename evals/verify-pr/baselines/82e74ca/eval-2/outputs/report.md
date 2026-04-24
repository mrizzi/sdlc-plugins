## Verification Report for TC-9102

**PR**: #743 -- Add severity threshold filter to advisory summary endpoint
**Task**: TC-9102
**Repository**: trustify-backend

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created |
| Scope Containment | FAIL | Task requires creating `tests/api/advisory_summary.rs` but no test file is present in the diff. The two modified files (`get.rs`, `advisory.rs`) are within scope. |
| Diff Size | PASS | Small, focused diff (~40 lines added across 2 files) |
| Commit Traceability | PASS | Commits reference TC-9102 |
| Sensitive Patterns | PASS | No passwords, API keys, secrets, or sensitive data found in the diff |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 2 of 6 criteria met (see breakdown below) |
| Test Quality | FAIL | No test file was created; task explicitly requires `tests/api/advisory_summary.rs` with 6 specific test cases |
| Test Change Classification | N/A | No test files present in the PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Acceptance Criteria Breakdown

| # | Criterion | Result | Issue |
|---|-----------|--------|-------|
| 1 | `?threshold=high` returns counts for critical and high only | FAIL | Filtering logic is inverted: the condition `threshold_idx <= severity_position` includes severities below the threshold instead of excluding them. Additionally, `total` is computed from unfiltered counts. |
| 2 | Without threshold, all severity counts returned (backward compatible) | PASS | `None` branch returns original summary unchanged. |
| 3 | `?threshold=invalid` returns 400 Bad Request | FAIL | Invalid values are silently accepted via `.unwrap_or(0)` and treated as `threshold=critical` instead of returning a 400 error. No input validation exists. |
| 4 | Severity ordering correct: critical > high > medium > low | FAIL | Ordering array is correctly defined but applied inversely in the filtering conditions, producing incorrect results for all threshold values. |
| 5 | Response includes `threshold_applied` boolean field | FAIL | Field is entirely absent from the response struct. Not implemented. |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | Existing fetch-or-404 logic is untouched by the changes. |

### Missing Implementation

1. **Input validation**: No validation of the `threshold` parameter. Invalid values are silently treated as `threshold=critical` via `.unwrap_or(0)` instead of returning 400 Bad Request using `AppError`.
2. **`threshold_applied` field**: The response does not include a `threshold_applied` boolean field to indicate whether filtering is active, as required by the acceptance criteria.
3. **Severity enum**: The implementation notes recommend defining a `Severity` enum with `Ord` trait, but the implementation uses a raw string array with incorrect index comparisons that invert the filtering logic.
4. **Test file**: `tests/api/advisory_summary.rs` is required by the task but is entirely absent from the diff. All six test scenarios specified in the Test Requirements are unaddressed.
5. **Total computation bug**: The `total` field in the filtered branch sums the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) instead of summing only the filtered counts.

### Overall: FAIL

The PR has critical defects that prevent it from meeting acceptance criteria. The filtering logic is inverted (produces incorrect results for all threshold values), there is no input validation for invalid threshold values, the required `threshold_applied` response field is missing entirely, and no test file was created despite the task requiring `tests/api/advisory_summary.rs` with six specific test cases. Only 2 of 6 acceptance criteria pass. This PR requires significant rework before it can be approved.
