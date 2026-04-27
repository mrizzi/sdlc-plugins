## Verification Report for TC-9102

**PR**: #743 -- Add severity threshold filter to advisory summary endpoint
**Task**: TC-9102
**Repository**: trustify-backend

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No review comments on this PR |
| Root-Cause Investigation | N/A | No sub-tasks created |
| Scope Containment | FAIL | Task requires creating `tests/api/advisory_summary.rs` but no test file appears in the diff. The two modified files (`get.rs`, `advisory.rs`) are within scope. |
| Diff Size | PASS | Small diff (~40 lines added across 2 files), proportionate to task scope |
| Commit Traceability | PASS | Commits reference TC-9102 |
| Sensitive Patterns | PASS | No passwords, API keys, secrets, or sensitive patterns detected in the diff |
| CI Status | PASS | All CI checks pass |
| Acceptance Criteria | FAIL | 2 of 6 criteria met (see breakdown below) |
| Test Quality | N/A | No test files present in the PR diff |
| Test Change Classification | N/A | No test files present in the PR diff |
| Verification Commands | N/A | No verification commands specified in task |

### Acceptance Criteria Breakdown

| # | Criterion | Result | Issue |
|---|-----------|--------|-------|
| 1 | `?threshold=high` returns counts for critical and high only | FAIL | Filtering logic is inverted: condition `threshold_idx <= severity_position` includes severities below the threshold instead of above. Additionally, `total` is computed from unfiltered counts. |
| 2 | Without threshold, all severity counts returned (backward compatible) | PASS | `None` branch returns original summary unchanged. |
| 3 | `?threshold=invalid` returns 400 Bad Request | FAIL | Invalid values are silently accepted via `.unwrap_or(0)` and treated as `threshold=critical` instead of returning 400. No input validation exists. |
| 4 | Severity ordering correct: critical > high > medium > low | FAIL | Ordering array is correctly defined but applied inversely in filtering logic, producing incorrect results. |
| 5 | Response includes `threshold_applied` boolean field | FAIL | Field is entirely absent from the response. Not implemented. |
| 6 | 404 for non-existent SBOM IDs (existing behavior preserved) | PASS | Existing fetch-or-404 logic is untouched by the changes. |

### Missing Implementation

1. **Input validation**: No validation of the `threshold` query parameter. Invalid values should return 400 Bad Request using `AppError`. Instead, `.unwrap_or(0)` silently maps unrecognized values to the "critical" threshold.
2. **`threshold_applied` field**: The `AdvisorySummary` response struct does not include a `threshold_applied` boolean field. This field is required by acceptance criteria to let API consumers distinguish filtered from unfiltered responses.
3. **Severity enum**: The implementation notes recommend a `Severity` enum implementing `Ord` for type-safe ordering. The implementation uses a raw string array with manual index comparisons, which led to the logic inversion bug.
4. **Test file**: `tests/api/advisory_summary.rs` is listed under "Files to Create" in the task but is entirely absent from the diff. All six specified test scenarios are unimplemented.
5. **Total computation bug**: The `total` in the filtered response sums unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) instead of the filtered values, so it always equals the unfiltered total regardless of the threshold applied.
6. **Inverted filtering logic**: The condition `threshold_idx <= N` includes severities at or below the threshold position rather than at or above it. The condition should be `N <= threshold_idx` to correctly retain only higher-severity counts.

### Overall: FAIL

The PR has critical defects across multiple acceptance criteria. The filtering logic is inverted (producing wrong results for all threshold values), there is no input validation for invalid threshold values, the required `threshold_applied` response field is missing, the total computation uses unfiltered counts, and the required test file was not created. Only 2 of 6 acceptance criteria pass (backward compatibility and 404 preservation). Scope containment also fails due to the missing test file. This PR requires significant rework before it can be approved.
