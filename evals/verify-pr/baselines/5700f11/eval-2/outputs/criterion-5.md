# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Result: FAIL

## Analysis

The task requires that the response includes a `threshold_applied` boolean field to indicate whether threshold filtering is active. This field should be `true` when a valid threshold parameter is provided and `false` (or absent) when no threshold is specified.

Examining the PR diff:

1. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`) is not modified in the diff. The diff for `advisory.rs` shows no structural changes to the response type.

2. The filtered response in `get.rs` constructs an `AdvisorySummary` with only the existing fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

No `threshold_applied` field is present in the response struct or in the constructed response object. This criterion is not satisfied.
