# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. The implementation defines a severity ordering array:

```rust
let severity_order = ["critical", "high", "medium", "low"];
```

And then uses `position()` to find the index of the requested threshold value. For `threshold=high`, this produces `threshold_idx = 1`.

The filtering logic is:

```rust
critical: summary.critical,                                    // always included
high: if threshold_idx <= 1 { summary.high } else { 0 },      // 1 <= 1 = true
medium: if threshold_idx <= 2 { summary.medium } else { 0 },  // 1 <= 2 = true
low: if threshold_idx <= 3 { summary.low } else { 0 },        // 1 <= 3 = true
```

When `threshold=high` (idx=1), the conditions evaluate as:
- `high`: `1 <= 1` = true (included) -- correct
- `medium`: `1 <= 2` = true (included) -- WRONG, should be excluded
- `low`: `1 <= 3` = true (included) -- WRONG, should be excluded

The logic is inverted. The comparisons should use `>=` (or the index comparison should be reversed) to include only severities at or above the threshold. As written, `threshold=high` returns all four severity counts instead of only critical and high.

The correct logic would compare each severity's index against the threshold index and include only those with index <= threshold_idx, but the comparison subjects are swapped. The threshold_idx should be compared as the upper bound for the severity index, not as a value being compared against hardcoded positions.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The filtering conditions `threshold_idx <= 1`, `threshold_idx <= 2`, `threshold_idx <= 3` are always true when threshold_idx is 0 or 1, meaning medium and low are never filtered out for critical or high thresholds.
- For threshold=critical (idx=0): high (0<=1=true), medium (0<=2=true), low (0<=3=true) -- all included, only critical should be returned.
- For threshold=high (idx=1): medium (1<=2=true), low (1<=3=true) -- both included, neither should be.
- The filtering only starts to work for threshold=medium (idx=2): low (2<=3=true) is still included, which is wrong.
- The logic never correctly filters any severity level.
