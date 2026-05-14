# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR implements threshold filtering in `modules/fundamental/src/advisory/endpoints/get.rs`, but the filtering logic is incorrect.

When `threshold=high`, the code sets `threshold_idx = 1` (position in `["critical", "high", "medium", "low"]`). The filtering then applies these conditions:

- `critical`: always included (no condition) -- correct
- `high`: `if threshold_idx <= 1` evaluates to `1 <= 1 = true` -- correct
- `medium`: `if threshold_idx <= 2` evaluates to `1 <= 2 = true` -- **INCORRECT**, medium should be excluded
- `low`: `if threshold_idx <= 3` evaluates to `1 <= 3 = true` -- **INCORRECT**, low should be excluded

The comparison is inverted. The correct condition should check whether each severity's index is within the threshold (e.g., `severity_index <= threshold_idx`), not whether `threshold_idx <= severity_index_literal`. As written, `threshold=high` still returns all four severity counts, defeating the purpose of the filter.

Additionally, the `total` field is computed as `summary.critical + summary.high + summary.medium + summary.low`, using unfiltered values regardless of the threshold. Even if the per-field filtering were correct, the total would not reflect the filtered counts.

Finally, the test file `tests/api/advisory_summary.rs` specified in the task's "Files to Create" section is entirely absent from the diff, so there are no integration tests to verify that `threshold=high` returns only critical and high counts.

## Evidence

- `get.rs` lines 41-54: filtering logic uses `threshold_idx <= N` instead of `N <= threshold_idx`
- `get.rs` line 52: `total` computed from unfiltered `summary.*` fields
- No test file in the diff to validate behavior
