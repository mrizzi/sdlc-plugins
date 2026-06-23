# Criterion 1: threshold=high returns counts for critical and high only

## Verdict: FAIL

## Reasoning

The acceptance criterion requires that `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only, omitting medium and low.

### Code Analysis

In `modules/fundamental/src/advisory/endpoints/get.rs`, the filtering logic is:

```rust
let severity_order = ["critical", "high", "medium", "low"];
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

For `threshold=high`, `position()` returns index 1. The comparisons evaluate as:
- critical: always included (hardcoded as `summary.critical`)
- high: `threshold_idx (1) <= 1` is true, so high is included (correct)
- medium: `threshold_idx (1) <= 2` is true, so medium is **included** (WRONG -- should be excluded)
- low: `threshold_idx (1) <= 3` is true, so low is **included** (WRONG -- should be excluded)

The comparison is inverted. The code checks `threshold_idx <= N` (where N is the severity's fixed index), but the correct logic should be `N <= threshold_idx` (include severity only if its position is at or above the threshold position). With the corrected logic for threshold=high (idx=1):
- high (N=1): `1 <= 1` is true -> included (correct)
- medium (N=2): `2 <= 1` is false -> excluded (correct)
- low (N=3): `3 <= 1` is false -> excluded (correct)

### Additional Bug: Total Computation

Even if the filtering comparisons were correct, the `total` field is computed from the **unfiltered** counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values. This means the total would not match the sum of the returned filtered counts.

### Conclusion

The filtering logic is fundamentally broken due to an inverted comparison. For threshold=high, all four severity levels are returned instead of only critical and high. This criterion is NOT satisfied.
