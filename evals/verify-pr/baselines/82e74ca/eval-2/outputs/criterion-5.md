## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Result: FAIL

### Analysis

The PR diff does not add a `threshold_applied` field to the response anywhere. The `AdvisorySummary` struct constructed in the filtered branch contains only the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The response fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field present.

The task acceptance criteria explicitly require this field so that API consumers can distinguish between a response that has been filtered by a threshold and one that returns all severity counts naturally. Without this field, a client receiving a response with zero counts for some severity levels cannot determine whether those severities genuinely have zero advisories or whether they were excluded by threshold filtering.

To satisfy this criterion, the `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`) would need to be extended with a `threshold_applied: bool` field. The handler would then need to set it to `true` when a threshold parameter is provided and `false` otherwise. Neither the struct modification nor the field assignment appears anywhere in the diff. This feature was not implemented at all.
