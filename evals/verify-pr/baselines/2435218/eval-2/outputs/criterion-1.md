# Criterion 1: Threshold filtering returns only severities at or above the threshold

**Criterion:** `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

**Verdict:** FAIL

## Analysis

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` implements threshold filtering logic in the `advisory_summary` handler. When a `threshold` query parameter is provided, the code uses a `severity_order` array `["critical", "high", "medium", "low"]` and finds the index of the threshold value.

The filtering logic sets severity counts to 0 for levels below the threshold index:

```rust
let threshold_idx = severity_order.iter()
    .position(|&s| s == threshold.to_lowercase())
    .unwrap_or(0);
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

For `?threshold=high`, the `threshold_idx` would be 1. This means:
- `critical`: always included (correct)
- `high`: included when `threshold_idx <= 1`, which is true for idx=1 (correct)
- `medium`: included when `threshold_idx <= 2`, which is true for idx=1 (INCORRECT -- medium should be excluded for threshold=high)
- `low`: included when `threshold_idx <= 3`, which is true for idx=1 (INCORRECT -- low should be excluded for threshold=high)

Wait -- re-reading more carefully: for `threshold=high`, idx=1. `medium` check is `if threshold_idx <= 2` which is `if 1 <= 2` = true, so medium IS included. This is wrong -- threshold=high should only return critical and high.

Actually, let me re-examine: The severity_order array is `["critical", "high", "medium", "low"]` with indices 0, 1, 2, 3. For threshold=high (idx=1):
- critical (idx 0): always included -- correct
- high (idx 1): `1 <= 1` = true, included -- correct
- medium (idx 2): `1 <= 2` = true, included -- WRONG, should be excluded
- low (idx 3): `1 <= 3` = true, included -- WRONG, should be excluded

The condition logic is inverted. The code checks `threshold_idx <= N` but it should check `N <= threshold_idx` (or equivalently `threshold_idx >= N`) to include only severities at index <= threshold_idx.

The correct logic should be: include a severity if its index in the ordering is <= threshold_idx. For high (idx 1), only critical (idx 0) and high (idx 1) should be included. The conditions should be:
- high: `1 <= threshold_idx` (i.e., threshold_idx >= 1)
- medium: `2 <= threshold_idx` (i.e., threshold_idx >= 2)
- low: `3 <= threshold_idx` (i.e., threshold_idx >= 3)

The actual code uses `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` which is the opposite -- it includes MORE severities as the threshold gets stricter (higher).

**However**, reconsidering: when threshold=critical (idx=0):
- high: `0 <= 1` = true (included) -- WRONG, should exclude
- medium: `0 <= 2` = true (included) -- WRONG
- low: `0 <= 3` = true (included) -- WRONG

When threshold=low (idx=3):
- high: `3 <= 1` = false (excluded) -- WRONG, should include
- medium: `3 <= 2` = false (excluded) -- WRONG
- low: `3 <= 3` = true (included) -- correct

The logic is completely inverted. The implementation effectively includes severities BELOW the threshold and excludes those ABOVE it, which is the opposite of the requirement.

Additionally, the `total` field is computed from the unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than the filtered values, which means the total is always the same regardless of threshold.

**Conclusion:** The filtering logic is inverted and the total calculation is incorrect. This criterion is NOT satisfied.
