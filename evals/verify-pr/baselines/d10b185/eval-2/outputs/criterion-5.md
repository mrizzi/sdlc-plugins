# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR does not add a `threshold_applied` boolean field to the response. The task acceptance criteria explicitly require this field to indicate whether threshold filtering is active.

Examining the diff:

1. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) is not modified in the diff. No new field is added to the response model.

2. The handler in `get.rs` constructs an `AdvisorySummary` in the `Some(threshold)` branch with only the existing fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

3. In the `None` branch, the unmodified `summary` is returned directly, which also lacks any `threshold_applied` field.

For this criterion to be satisfied, the `AdvisorySummary` struct would need a `threshold_applied: bool` field, set to `true` when a threshold parameter is provided and `false` otherwise. Neither the struct modification nor the field assignment appears anywhere in the diff.

## Evidence

- No modification to `AdvisorySummary` struct in the diff (the model file `modules/fundamental/src/advisory/model/summary.rs` is not changed)
- `get.rs` lines 47-53: constructed `AdvisorySummary` has no `threshold_applied` field
- `get.rs` line 55: `None => summary` returns original struct, also without `threshold_applied`
