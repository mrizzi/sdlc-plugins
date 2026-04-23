# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Result: FAIL

## Analysis

The PR introduces threshold filtering in `modules/fundamental/src/advisory/endpoints/get.rs`. The filtering logic uses a `severity_order` array `["critical", "high", "medium", "low"]` where critical=index 0, high=index 1, medium=index 2, low=index 3.

For `threshold=high`, `threshold_idx` resolves to 1. The code then applies these conditions:

- `critical`: always included (no conditional) -- correct
- `high`: `if threshold_idx <= 1` => `1 <= 1` => true -- included (correct)
- `medium`: `if threshold_idx <= 2` => `1 <= 2` => true -- **included (INCORRECT)**
- `low`: `if threshold_idx <= 3` => `1 <= 3` => true -- **included (INCORRECT)**

The filtering logic is inverted. The condition `threshold_idx <= N` (where N is the severity's position in the array) checks whether the threshold is at or above the severity's position, which means nearly all severities pass the filter for any threshold value. The correct condition should be `N <= threshold_idx` (include the severity only if its index is at or below the threshold's index, meaning it is at least as severe as the threshold).

With `threshold=high`, the endpoint returns counts for critical, high, medium, AND low -- not just critical and high as required. This criterion is not satisfied.

Additionally, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) regardless of filtering, which compounds the incorrectness even if the individual field conditions were fixed.
