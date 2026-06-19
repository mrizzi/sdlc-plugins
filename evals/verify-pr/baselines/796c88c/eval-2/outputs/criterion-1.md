# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## What was checked

Inspected the PR diff in `get.rs` for the filtering logic when a `threshold` query parameter is provided.

## Evidence

The diff adds a `SummaryParams` struct with an `Option<String>` threshold field and a `Query(params)` extractor to the `advisory_summary` handler. The filtering logic uses a `severity_order` array `["critical", "high", "medium", "low"]` and finds the position of the threshold value. When `threshold=high`, `threshold_idx` would be 1, and the logic is:

- `critical`: always included (no conditional)
- `high`: included if `threshold_idx <= 1` (1 <= 1, true, so included)
- `medium`: included if `threshold_idx <= 2` (1 <= 2, true -- this SHOULD be excluded for threshold=high)
- `low`: included if `threshold_idx <= 3` (1 <= 3, true -- this SHOULD be excluded for threshold=high)

Wait -- re-examining the logic more carefully:

The `severity_order` is `["critical", "high", "medium", "low"]`. For `threshold=high`, `threshold_idx = 1`.

- `high`: `threshold_idx <= 1` => `1 <= 1` => true => included (correct)
- `medium`: `threshold_idx <= 2` => `1 <= 2` => true => included (INCORRECT -- medium should be excluded when threshold is high)
- `low`: `threshold_idx <= 3` => `1 <= 3` => true => included (INCORRECT -- low should be excluded when threshold is high)

The logic is inverted. The condition should be checking if the severity's index is <= threshold_idx, not if threshold_idx <= severity's index. The current implementation includes severities BELOW the threshold instead of excluding them.

Actually, let me reconsider. The intended semantics is "include only severities at or above the threshold." The severity order is critical(0) > high(1) > medium(2) > low(3). For threshold=high (idx=1), we want to include severities with index <= 1 (critical and high). The conditions should check if EACH severity's own index is <= threshold_idx:

- critical (idx 0): 0 <= 1? yes => include (correct, always included in the code)
- high (idx 1): 1 <= 1? yes => include (code checks threshold_idx <= 1, i.e., 1 <= 1, same result)
- medium (idx 2): 2 <= 1? no => exclude (but code checks threshold_idx <= 2, i.e., 1 <= 2, which is TRUE => INCORRECTLY includes medium)
- low (idx 3): 3 <= 1? no => exclude (but code checks threshold_idx <= 3, i.e., 1 <= 3, which is TRUE => INCORRECTLY includes low)

The filtering logic is inverted. The comparisons check `threshold_idx <= severity_position` instead of `severity_position <= threshold_idx`. This means for `threshold=high`, medium and low are incorrectly included.

## Verdict: FAIL

The filtering logic is inverted. When `threshold=high`, the implementation incorrectly includes medium and low counts instead of filtering them out. The condition `threshold_idx <= N` should be `N <= threshold_idx` (or equivalently, the severity's index should be compared against the threshold index, not the reverse).
