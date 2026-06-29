# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Result: FAIL

## Analysis

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` adds threshold filtering logic that attempts to implement this criterion. The relevant code is:

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

When `threshold=high`, `threshold_idx` would be 1. This means:
- `critical`: always included (correct)
- `high`: included because `1 <= 1` is true (correct)
- `medium`: excluded because `1 <= 2` is true -- wait, this is WRONG. `threshold_idx` is 1, and `1 <= 2` evaluates to `true`, so `medium` would be INCLUDED when threshold=high.

Actually, re-examining: the logic zeroes out values where the threshold index is NOT less than or equal to the severity's position. For `threshold=high` (index 1):
- `critical`: always kept
- `high`: `1 <= 1` = true, so kept
- `medium`: `1 <= 2` = true, so kept -- THIS IS WRONG. Medium should be excluded when threshold=high.

Wait, let me re-read the code. The condition is `if threshold_idx <= N`. For threshold=high (idx=1):
- high: `1 <= 1` = true, high is kept (correct)
- medium: `1 <= 2` = true, medium is kept (WRONG -- should be excluded)
- low: `1 <= 3` = true, low is kept (WRONG -- should be excluded)

The filtering logic is inverted. The conditions should be `if N <= threshold_idx` or `if threshold_idx >= N` to correctly filter out severities below the threshold. As implemented, `threshold=high` would return ALL four counts, not just critical and high.

Additionally, the `total` field is computed from unfiltered counts (`summary.critical + summary.high + summary.medium + summary.low`) rather than from the filtered values, so even if the per-severity filtering were correct, the total would be wrong.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines in the `Some(threshold)` match arm
- The condition `threshold_idx <= N` passes for all N >= threshold_idx, meaning severities BELOW the threshold are included rather than excluded
- The `total` field uses unfiltered counts

## Conclusion

The filtering logic is buggy: the comparison direction means that setting `threshold=high` would still return medium and low counts. The criterion requires that only critical and high counts are returned, which this implementation does not achieve correctly. Additionally the total is always the sum of all four unfiltered counts.
