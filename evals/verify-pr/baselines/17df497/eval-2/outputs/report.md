## Verification Report for TC-9102

**PR**: #743 — Add severity threshold filter to advisory summary endpoint
**Task**: TC-9102
**Repository**: trustify-backend

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments |
| Root-Cause Investigation | N/A | No sub-tasks created |
| Scope Containment | FAIL | Task requires creating `tests/api/advisory_summary.rs` but no test file is present in the diff. Modified files (`get.rs`, `advisory.rs`) are within scope. |
| Diff Size | PASS | Small, focused diff (~40 lines added across 2 files |
| Commit Traceability | PASS | Commits reference TC-9102 |
| Sensitive Patterns | PASS | No passwords, API keys, secrets, or sensitive data found in the diff |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 2 of 6 criteria met (see breakdown below) |
| Test Quality | FAIL | No test file was created; task explicitly requires `tests/api/advisory_summary.rs` with 6 specific test cases |
| Test Change Classification | N/A | No test files present in the PR diff |
| Verification Commands | N/A | Cannot execute commands against target repository |

### Acceptance Criteria Breakdown

| # | Criterion | Result | Issue |
|---|-----------|--------|-------|
| 1 | `?threshold=high` returns counts for critical and high only | FAIL | Filtering logic is inverted: condition `threshold_idx <= severity_position` includes severities below the threshold instead of excluding them. Also, `total` is computed from unfiltered counts. |
| 2 | Without threshold, all severity counts returned (backward compatible) | PASS | `None` branch returns original summary unchanged. |
| 3 | `?threshold=invalid` returns 400 Bad Request | FAIL | Invalid values are silently accepted via `.unwrap_or(0)`, treated as `threshold=critical` instead of returning 400. No input validation exists. |
| 4 | Severity ordering correct: critical > high > medium > low | FAIL | Ordering array is defined correctly but applied inversely in the filtering logic, producing incorrect results. |
| 5 | Response includes `threshold_applied` boolean field | FAIL | Field is entirely absent from the response struct. Not implemented. |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | Existing fetch-or-404 logic is untouched by the changes. |

### Missing Implementation

1. **Input validation**: No validation of the `threshold` parameter. Invalid values should return 400 Bad Request using `AppError`.
2. **`threshold_applied` field**: The response does not include a boolean field to indicate whether filtering is active.
3. **Severity enum**: The implementation notes recommend a `Severity` enum with `Ord`, but the implementation uses a raw string array with incorrect index comparisons.
4. **Test file**: `tests/api/advisory_summary.rs` is required by the task but entirely absent from the diff. All six test scenarios are unaddressed.
5. **Total computation bug**: The `total` in the filtered branch sums unfiltered counts instead of filtered counts.

### Overall: FAIL

The PR has critical defects that prevent it from meeting acceptance criteria. The filtering logic is inverted (produces wrong results for all threshold values), there is no input validation for invalid threshold values, the `threshold_applied` response field is missing, and no test file was created. Only 2 of 6 acceptance criteria pass. This PR requires significant rework before it can be approved.
