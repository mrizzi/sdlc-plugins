## Criterion 5

**Text**: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict**: FAIL

**Reasoning**:

The response does NOT include a `threshold_applied` boolean field. Examining the `AdvisorySummary` struct construction in the filtered branch of `modules/fundamental/src/advisory/endpoints/get.rs`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The response struct only contains five fields: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the diff.

To satisfy this criterion, the implementation would need to:

1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs`, which is not modified in this diff).
2. Set `threshold_applied: true` in the `Some(threshold)` branch.
3. Set `threshold_applied: false` in the `None` branch (or in the original `summary` construction in `advisory.rs`).

Neither the model struct nor the endpoint handler includes this field. The `advisory.rs` service file diff also shows no addition of this field to the `AdvisorySummary` construction in `aggregate_severities`.

This is a clear acceptance criteria failure — the required response field is entirely absent.
