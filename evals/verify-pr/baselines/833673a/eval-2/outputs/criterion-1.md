# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. When a threshold parameter is provided, the code looks up the threshold string in a `severity_order` array and uses the resulting index to decide which severity counts to include.

The severity_order array is defined as `["critical", "high", "medium", "low"]`, so for `threshold=high`, the index is 1.

The filtering logic uses these conditions:
- `critical`: always included (no condition)
- `high`: included if `threshold_idx <= 1`
- `medium`: included if `threshold_idx <= 2`
- `low`: included if `threshold_idx <= 3`

For `threshold=high` (idx=1):
- `critical`: always included (correct)
- `high`: `1 <= 1` = true, included (correct)
- `medium`: `1 <= 2` = true, included (INCORRECT -- should be excluded)
- `low`: `1 <= 3` = true, included (INCORRECT -- should be excluded)

The comparison is inverted. The code checks whether `threshold_idx <= severity_position` when it should check whether `severity_position <= threshold_idx`. As a result, when `threshold=high`, all four severity levels are returned instead of only critical and high.

The correct conditions should be:
- `high`: included if `1 <= threshold_idx` (i.e., severity index 1 <= threshold index)
- `medium`: included if `2 <= threshold_idx`
- `low`: included if `3 <= threshold_idx`

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered counts, so even if the filtering were correct, the total would still be wrong.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- Lines: The match arm constructing the filtered `AdvisorySummary`
- The conditions `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` are all true when `threshold_idx` is 0 or 1, meaning no filtering occurs for `threshold=high` or `threshold=critical`
