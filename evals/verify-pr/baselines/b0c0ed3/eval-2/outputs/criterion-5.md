## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Result: FAIL

### Analysis

The PR diff does not add a `threshold_applied` field to the response anywhere. The `AdvisorySummary` struct constructed in the filtered branch contains only:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The response fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field.

The acceptance criteria explicitly require this field so that API consumers can programmatically determine whether the response has been filtered. Without it, a client receiving a response where some severity counts are zero cannot distinguish between genuinely zero advisories and filtered-out severities.

To satisfy this criterion, the `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`) would need to be updated to include a `threshold_applied: bool` field. The filtered code path should set this to `true`, and the unfiltered path should set it to `false`. None of this work appears in the diff.

This is an entirely missing feature, not a partial implementation.
