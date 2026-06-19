# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The PR adds a threshold filtering mechanism in `modules/fundamental/src/advisory/endpoints/get.rs`, but the filtering logic is **inverted**, causing incorrect results.

### How the code works

The code defines a severity ordering array: `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3 respectively. For `threshold=high`, `threshold_idx` is resolved to `1`.

The filtering conditions are:
- `critical`: always included (no condition)
- `high`: included if `threshold_idx <= 1`
- `medium`: included if `threshold_idx <= 2`
- `low`: included if `threshold_idx <= 3`

### Why this is wrong

For `threshold=high` (`threshold_idx = 1`):
- `high`: `1 <= 1` = true -- included (correct)
- `medium`: `1 <= 2` = true -- included (WRONG, should be excluded)
- `low`: `1 <= 3` = true -- included (WRONG, should be excluded)

The condition checks whether the threshold's index is less than or equal to each severity's hardcoded position. The correct logic should check whether each severity's position is less than or equal to the threshold index:
- `high` (position 1): `1 <= threshold_idx(1)` = true (correct)
- `medium` (position 2): `2 <= threshold_idx(1)` = false (correct -- excluded)
- `low` (position 3): `3 <= threshold_idx(1)` = false (correct -- excluded)

### Additional bug: total computation

The `total` field in the filtered summary is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. Even if the filtering conditions were corrected, the total would not match the sum of the returned severity counts.

### Conclusion

The filtering logic is inverted. With `threshold=high`, the endpoint returns all four severity counts instead of only critical and high. This criterion is not satisfied.
