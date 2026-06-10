# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR diff does not add a `threshold_applied` boolean field to the `AdvisorySummary` response struct. The filtered response is constructed with only the existing fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the diff.

To satisfy this criterion, the `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`) would need a new `threshold_applied: bool` field, and the handler would need to set it to `true` when a threshold parameter is provided and `false` when it is not.

Neither the model modification nor the field assignment appears in the diff. The criterion is not satisfied.
