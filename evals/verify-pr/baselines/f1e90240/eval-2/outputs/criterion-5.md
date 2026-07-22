# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The task description requires that the API response include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be `true` when a threshold parameter is provided and `false` (or absent) when no threshold is specified.

Examining the PR diff, the `AdvisorySummary` struct constructed in the filtered response contains only:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Additionally, the `None` branch returns the original `summary` unchanged, which also would not include a `threshold_applied` field.

### Expected implementation

The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) would need to be extended with a `threshold_applied: bool` field. The endpoint handler would then set:
- `threshold_applied: true` when `params.threshold` is `Some(_)`
- `threshold_applied: false` when `params.threshold` is `None`

Neither the struct modification nor the field assignment appears anywhere in the PR diff.

## Conclusion

This criterion is **not satisfied**. The response does not include a `threshold_applied` boolean field. The `AdvisorySummary` struct was not modified to include this field, and the endpoint handler does not set it.
