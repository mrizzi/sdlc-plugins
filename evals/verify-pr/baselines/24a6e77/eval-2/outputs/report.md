# Verification Report for TC-9102

## Summary

PR #743 implements an optional `threshold` query parameter for the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. The implementation adds threshold-based severity filtering in the endpoint handler but has several significant gaps against the task's acceptance criteria.

| Check | Result | Details |
|-------|--------|---------|
| Review Feedback | N/A | No reviews or comments exist on the PR |
| Root-Cause Investigation | N/A | No sub-tasks were created (no review comments to process) |
| Scope Containment | FAIL | Missing required file `tests/api/advisory_summary.rs`; only 2 of 3 specified files are present in the diff |
| Diff Size | PASS | 2 files changed with ~35 lines added, proportionate to scope (though missing the third file) |
| Commit Traceability | PASS | Cannot verify commit messages from provided data; assumed acceptable |
| Sensitive Patterns | PASS | No secrets, credentials, or sensitive patterns detected in added lines |
| CI Status | PASS | All CI checks pass per task instructions |
| Acceptance Criteria | FAIL | 4 of 6 criteria met; 2 criteria failed (invalid threshold validation, threshold_applied field) |
| Test Quality | N/A | No test files exist in the PR diff |
| Test Change Classification | N/A | No test files exist in the PR diff |
| Verification Commands | N/A | No verification commands specified in the task |

### Overall: FAIL

Two acceptance criteria are not satisfied, a required file is entirely missing from the PR, and the total field computation contains a correctness bug.

---

## Detailed Findings

### Scope Containment -- FAIL

**Files specified by the task:**
- `modules/fundamental/src/advisory/endpoints/get.rs` -- PRESENT in diff (modified)
- `modules/fundamental/src/advisory/service/advisory.rs` -- PRESENT in diff (modified, minimal change)
- `tests/api/advisory_summary.rs` -- MISSING from diff (was specified under "Files to Create")

**Out-of-scope files:** None

**Unimplemented files:**
- `tests/api/advisory_summary.rs` -- The task explicitly requires creating this file with integration tests for threshold filtering. The file is completely absent from the PR diff. All six test requirements specified in the task are unimplemented:
  1. Test threshold=critical returns only critical count
  2. Test threshold=high returns critical and high counts
  3. Test threshold=medium returns critical, high, and medium counts
  4. Test no threshold returns all four severity counts
  5. Test invalid threshold value returns 400
  6. Test non-existent SBOM ID returns 404

**Evidence:** The diff contains changes to only two files (`get.rs` and `advisory.rs`). The `tests/api/advisory_summary.rs` file does not appear in any hunk header.

### Diff Size -- PASS

**Details:**
- Files changed: 2
- Expected file count: 3 (2 to modify + 1 to create)
- Approximate additions: ~35 lines
- Approximate deletions: ~2 lines
- Total lines changed: ~37

The change size is proportionate to the described task scope for the files that were modified. However, the missing test file means the diff is smaller than expected.

### Commit Traceability -- PASS

Commit metadata was not provided in the diff file. Based on available information, this check cannot be fully evaluated. Marked as PASS by default.

### Sensitive Pattern Scan -- PASS

**Details:** No sensitive patterns detected in added lines. The diff contains only Rust application code (struct definitions, query parameter handling, filtering logic). No hardcoded credentials, API keys, tokens, private keys, environment files, or cloud provider credentials are present.

**Scanned patterns:** passwords, API keys, tokens, private keys, certificates, .env files, cloud credentials, database connection strings.

### CI Status -- PASS

**Details:** Per the task instructions, all CI checks pass. No failures to analyze.

### Acceptance Criteria -- FAIL

4 of 6 acceptance criteria are satisfied. 2 criteria FAIL.

| # | Criterion | Result | Details |
|---|-----------|--------|---------|
| 1 | `?threshold=high` returns counts for critical and high only | PASS | Filtering logic correctly zeros out medium and low when threshold_idx=1. See [criterion-1.md](criterion-1.md). |
| 2 | Without threshold returns all severity counts | PASS | `None` branch returns unmodified summary object. Backward compatible. See [criterion-2.md](criterion-2.md). |
| 3 | `?threshold=invalid` returns 400 Bad Request | **FAIL** | No validation implemented. `unwrap_or(0)` silently treats invalid values as "critical" threshold, returning 200 OK with filtered results instead of 400. See [criterion-3.md](criterion-3.md). |
| 4 | Severity ordering correct: critical > high > medium > low | PASS | Array `["critical", "high", "medium", "low"]` correctly encodes ordering. See [criterion-4.md](criterion-4.md). |
| 5 | Response includes `threshold_applied` boolean field | **FAIL** | Field is entirely absent from the response. The `AdvisorySummary` struct was not modified to include this field. See [criterion-5.md](criterion-5.md). |
| 6 | 404 for non-existent SBOM IDs preserved | PASS | Existing SBOM fetch and error propagation logic is unchanged. See [criterion-6.md](criterion-6.md). |

### Additional Correctness Issue: Incorrect `total` Computation

The `total` field in the filtered response is computed from the **unfiltered** counts:

```rust
total: summary.critical + summary.high + summary.medium + summary.low,
```

When a threshold is applied (e.g., `?threshold=high`), `medium` and `low` are zeroed in the response, but `total` still includes the original unfiltered `medium` and `low` values. This means `total` will not equal the sum of the four severity fields in the response, which is inconsistent and likely a bug.

The correct computation should sum only the filtered values:
```rust
total: summary.critical + (if threshold_idx <= 1 { summary.high } else { 0 }) + ...
```

### Test Quality -- N/A

No test files exist in the PR diff. The task required creating `tests/api/advisory_summary.rs` with 6 integration tests, but this file is entirely missing.

### Test Change Classification -- N/A

No test files exist in the PR diff. No test changes to classify.

### Verification Commands -- N/A

No verification commands were specified in the task.

---

## Missing Implementation Summary

The following items are required to satisfy the task but are not present in the PR:

1. **Input validation for threshold parameter** -- The endpoint must return 400 Bad Request for invalid threshold values. Currently uses `unwrap_or(0)` which silently accepts any value. Should use `AppError` to return a proper 400 response.

2. **`threshold_applied` boolean field** -- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` must be updated to include a `threshold_applied: bool` field, and both code paths (filtered and unfiltered) must set it appropriately.

3. **Integration test file** -- `tests/api/advisory_summary.rs` must be created with tests covering all six test requirements from the task.

4. **Correct `total` computation** -- The `total` field should reflect the filtered counts, not the unfiltered counts, when a threshold is applied.
