## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Result: FAIL

### Analysis

The PR diff does not add a `threshold_applied` field to the response at any point. The `AdvisorySummary` struct constructed in the filtered branch contains only the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field.

The task acceptance criteria explicitly require this field so that API consumers can distinguish between a response that has been filtered and one that has not. Without this field, a client receiving a response with zero counts for some severities cannot tell whether those severities genuinely have zero advisories or whether they were filtered out by a threshold.

The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`) would need to be updated to include this field, and both the filtered and unfiltered code paths would need to set it appropriately (`true` when a threshold is applied, `false` otherwise). None of this work was done.
