# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The acceptance criterion requires the response to include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field is completely absent from the implementation.

The `AdvisorySummary` struct constructed in the filtered case contains only:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

To satisfy this criterion, the `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`) would need a `threshold_applied: bool` field added, and the handler would need to set it to `true` when a threshold parameter is provided and `false` otherwise.

Neither the model struct modification nor the field assignment appears anywhere in the PR diff.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the constructed `AdvisorySummary` has no `threshold_applied` field
- File: `modules/fundamental/src/advisory/model/summary.rs` -- NOT modified in the PR diff (no struct changes)
- The `None` arm returns `summary` directly, which also lacks `threshold_applied`
- No changes to the `AdvisorySummary` struct definition appear anywhere in the diff
