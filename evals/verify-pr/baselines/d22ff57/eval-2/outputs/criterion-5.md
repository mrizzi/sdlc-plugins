# Criterion 5

**Text**: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Evidence from diff**:

The diff constructs the filtered `AdvisorySummary` as:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in the constructed response struct. The `AdvisorySummary` struct only contains `critical`, `high`, `medium`, `low`, and `total` fields. No modification to the `AdvisorySummary` model (in `modules/fundamental/src/advisory/model/summary.rs`) appears in the diff to add this field.

The `None` branch also returns `summary` without any `threshold_applied` field.

This required field is entirely absent from the implementation.

**Verdict**: FAIL
