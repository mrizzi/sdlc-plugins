# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Result: FAIL

## Reasoning

The diff implements threshold filtering in `get.rs`, but the filtering logic is inverted.

The severity order array is defined as `["critical", "high", "medium", "low"]`, giving indices:
- critical = 0
- high = 1
- medium = 2
- low = 3

For `threshold=high`, `threshold_idx = 1`.

The filtering conditions are:
- `critical`: always included (no condition) -- correct
- `high`: included if `threshold_idx <= 1` -> `1 <= 1` = true -- correct
- `medium`: included if `threshold_idx <= 2` -> `1 <= 2` = true -- **WRONG** (medium should be excluded for threshold=high)
- `low`: included if `threshold_idx <= 3` -> `1 <= 3` = true -- **WRONG** (low should be excluded for threshold=high)

The logic checks whether `threshold_idx <= severity_position`, but it should check whether `severity_position <= threshold_idx` (i.e., include the severity only if it ranks at or above the threshold). As implemented, `threshold=high` would still return counts for all four severities, defeating the purpose of the filter.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the per-severity filtering were correct, the total would be wrong.
