## Verification Report for TC-9102

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No reviews or comments exist on the PR |
| Root-Cause Investigation | N/A | No sub-tasks created from review feedback |
| Scope Containment | FAIL | Task-required file `tests/api/advisory_summary.rs` is missing from PR diff |
| Diff Size | PASS | 2 files changed; proportionate to task scope (3 expected files minus the missing test file) |
| Commit Traceability | PASS | Unable to verify commit messages (no commit metadata available in eval context); assumed PASS based on available data |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass per eval scenario |
| Acceptance Criteria | FAIL | 3 of 6 criteria not met (see details below) |
| Test Quality | N/A | No test files exist in the PR diff |
| Test Change Classification | N/A | No test files exist in the PR diff |
| Verification Commands | N/A | No verification commands specified in task |

### Overall: FAIL

The PR fails verification due to multiple missing acceptance criteria and a missing required file.

---

## Detailed Findings

### Scope Containment -- FAIL

**Details:** The task specifies 3 files: 2 to modify and 1 to create. The PR diff contains only 2 of the 3 required files.

**Files in PR diff:**
- `modules/fundamental/src/advisory/endpoints/get.rs` (modified) -- PRESENT
- `modules/fundamental/src/advisory/service/advisory.rs` (modified) -- PRESENT

**Files missing from PR diff:**
- `tests/api/advisory_summary.rs` (to create) -- MISSING

**Evidence:** The task description under "Files to Create" explicitly requires:
> `tests/api/advisory_summary.rs` -- integration tests for threshold filtering

This file is entirely absent from the PR diff. No test file of any kind was added or modified. The task also specifies 6 test requirements (threshold=critical, threshold=high, threshold=medium, no threshold, invalid threshold, non-existent SBOM), none of which can be verified without the test file.

**Related review comments:** none

### Diff Size -- PASS

**Details:** The PR modifies 2 files with a modest number of changes, which is proportionate for adding a query parameter and filtering logic to an existing endpoint.

**Evidence:**
- Files changed: 2
- Expected files: 3 (2 to modify + 1 to create)
- The diff size is small and focused, consistent with the task scope (minus the missing test file)

**Related review comments:** none

### Sensitive Patterns -- PASS

**Details:** No sensitive patterns detected in added lines across 2 files.

**Evidence:** Scanned all added lines in the diff for hardcoded passwords, API keys, tokens, private keys, environment file additions, cloud provider credentials, and database credentials. No matches found. The diff contains only Rust source code with query parameter handling and filtering logic.

**Related review comments:** none

### CI Status -- PASS

**Details:** All CI checks pass per the eval scenario specification.

**Related review comments:** none

### Acceptance Criteria -- FAIL

3 of 6 acceptance criteria are not met.

#### Criterion 1: Threshold filtering returns correct counts -- FAIL

**Requirement:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only.

**Finding:** The filtering logic in `get.rs` uses inverted comparison logic. The code checks `threshold_idx <= N` for each severity level, but this is backwards. For `threshold=high` (index 1):
- `threshold_idx <= 1` (high) = true -- included (correct)
- `threshold_idx <= 2` (medium) = true -- included (**incorrect**, should be excluded)
- `threshold_idx <= 3` (low) = true -- included (**incorrect**, should be excluded)

The correct condition should be `N <= threshold_idx` (include severity at position N only if N is at or above the threshold position). With the current logic, only `threshold=critical` (index 0) produces correct filtering; all other threshold values include too many severities.

Additionally, the `total` field is computed from unfiltered counts regardless of the threshold:
```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```
This should sum only the filtered counts.

#### Criterion 2: No threshold returns all counts -- PASS

**Requirement:** `GET /api/v2/sbom/{id}/advisory-summary` without threshold returns all severity counts (backward compatible).

**Finding:** The `None` arm of the match returns the unfiltered `summary` directly, preserving backward compatibility.

#### Criterion 3: Invalid threshold returns 400 -- FAIL

**Requirement:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=invalid` returns 400 Bad Request.

**Finding:** Invalid threshold values are silently accepted. The code uses `.unwrap_or(0)` when the threshold string is not found in the severity array, defaulting to index 0 (critical-level filtering) instead of returning a 400 error:
```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
```

The task explicitly requires returning 400 for invalid values and references `common/src/error.rs::AppError` for validation errors. No validation, no `Err(...)` return, and no reference to `AppError` exists in the diff.

#### Criterion 4: Severity ordering -- PASS

**Requirement:** Severity ordering is correct: critical > high > medium > low.

**Finding:** The array `["critical", "high", "medium", "low"]` correctly represents the ordering with critical at index 0 (highest) and low at index 3 (lowest). The task recommended a `Severity` enum with `Ord`, which was not implemented, but the ordering values themselves are correct.

#### Criterion 5: `threshold_applied` boolean field -- FAIL

**Requirement:** Response includes a `threshold_applied` boolean field indicating whether filtering is active.

**Finding:** The `threshold_applied` field is completely absent from the PR diff. The `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`) is not modified to include this field, and neither branch of the match expression sets such a field. The response schema is unchanged from the pre-threshold version.

#### Criterion 6: 404 for non-existent SBOM IDs -- PASS

**Requirement:** Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved).

**Finding:** The existing SBOM fetch logic (`SbomService::new(&db).fetch(sbom_id.id)`) is preserved unchanged in the diff. The threshold filtering code executes only after a successful SBOM lookup, so the 404 path remains intact.

### Test Quality -- N/A

**Details:** No test files exist in the PR diff. The required test file `tests/api/advisory_summary.rs` was not created. All 6 test requirements from the task specification are unverified:
- Test threshold=critical returns only critical count
- Test threshold=high returns critical and high counts
- Test threshold=medium returns critical, high, and medium counts
- Test no threshold returns all four severity counts
- Test invalid threshold value returns 400
- Test non-existent SBOM ID returns 404

### Test Change Classification -- N/A

**Details:** No test files exist in the PR diff. The PR modifies only production code files (`get.rs` and `advisory.rs`). Since there are no test files to classify, this check is not applicable.

### Verification Commands -- N/A

**Details:** No verification commands were specified in the task description. No eval infrastructure changes were detected in the PR diff.

---

## Summary of Failures

1. **Acceptance Criteria FAIL (3 of 6 criteria not met):**
   - Criterion 1: Threshold filtering logic is inverted -- `threshold=high` still includes medium and low counts
   - Criterion 3: Invalid threshold values are silently accepted (`.unwrap_or(0)`) instead of returning 400 Bad Request
   - Criterion 5: `threshold_applied` boolean field is entirely missing from the response

2. **Scope Containment FAIL:**
   - `tests/api/advisory_summary.rs` is listed under "Files to Create" but is absent from the PR diff
   - All 6 test requirements from the task specification are unimplemented

3. **Additional concern (total computation):**
   - The `total` field in the filtered response sums unfiltered counts instead of filtered counts, producing incorrect totals when a threshold is applied
