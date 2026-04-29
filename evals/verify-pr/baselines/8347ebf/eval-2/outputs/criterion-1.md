# Criterion 1: `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns counts for critical and high only

## Verdict: FAIL

## Analysis

The PR adds threshold filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`. When the `threshold` query parameter is provided, the code looks up its index in the `severity_order` array `["critical", "high", "medium", "low"]` (indices 0, 1, 2, 3 respectively) and then conditionally zeroes out severity counts based on comparisons against that index.

### The filtering logic (from the diff):

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

### Problem: Inverted comparison logic

For `threshold=high`, `threshold_idx` = 1. The conditions evaluate as follows:

| Severity | Condition | Evaluation | Result | Expected |
|----------|-----------|------------|--------|----------|
| critical | always included | -- | INCLUDED | INCLUDED |
| high | `1 <= 1` | true | INCLUDED | INCLUDED |
| medium | `1 <= 2` | true | INCLUDED | EXCLUDED |
| low | `1 <= 3` | true | INCLUDED | EXCLUDED |

The comparisons are inverted. The condition `threshold_idx <= severity_idx` evaluates to true for severities at or BELOW the threshold, not at or ABOVE. The correct logic should check whether each severity's index is less than or equal to the threshold index (i.e., the severity is at least as severe as the threshold). The conditions should be something like `if 1 <= threshold_idx` for high (severity index <= threshold index), `if 2 <= threshold_idx` for medium, etc. -- or equivalently, `threshold_idx >= severity_index`.

As implemented, `threshold=high` would include ALL four severity levels (critical, high, medium, low), which is identical to no filtering at all. The criterion requires that only `critical` and `high` counts are returned.

### Additional issue: Total uses unfiltered counts

Even if the filtering logic were corrected, the `total` field is computed from the unfiltered values (`summary.critical + summary.high + summary.medium + summary.low`) instead of the filtered values. This means the total would not match the sum of the returned counts.

## Conclusion

This criterion is NOT satisfied. The filtering logic is inverted, causing `threshold=high` to include medium and low counts instead of excluding them.
