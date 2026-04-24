## Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

### Result: FAIL

### Analysis

The filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs` is inverted.

The severity order array is defined as `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3 respectively (lower index = higher severity). For `threshold=high`, the `threshold_idx` resolves to 1.

The code then applies the following conditions:

- `critical`: always included (hardcoded as `summary.critical`)
- `high`: `if threshold_idx <= 1` -- evaluates to `1 <= 1` = true -- included
- `medium`: `if threshold_idx <= 2` -- evaluates to `1 <= 2` = true -- **incorrectly included**
- `low`: `if threshold_idx <= 3` -- evaluates to `1 <= 3` = true -- **incorrectly included**

The condition `threshold_idx <= severity_position` is backwards. To correctly filter severities at or above the threshold, the condition should be `severity_position <= threshold_idx` (i.e., include only severities whose index is at most the threshold index).

With the current logic, `threshold=high` would include ALL severity levels instead of only critical and high. The filtering effectively does nothing for any threshold other than `low` (and even `low` would include everything since all positions satisfy `3 <= N` only for `low` itself -- actually `3 <= 1` is false, `3 <= 2` is false, `3 <= 3` is true, so threshold=low would give critical + low, which is also wrong).

This is a fundamental logic bug that causes the criterion to fail.

Additionally, the `total` field in the filtered `AdvisorySummary` is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`), so even if the filtering were fixed, the total would not reflect the filtered values.
