# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR diff constructs an `AdvisorySummary` struct in the filtered case with the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in this struct construction. The fields present are: `critical`, `high`, `medium`, `low`, and `total`. The acceptance criterion explicitly requires a `threshold_applied` boolean field to indicate whether filtering is active.

Additionally, the `AdvisorySummary` model (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) would need to be updated to include this new field, and that file does not appear in the PR diff at all.

## Evidence

The `AdvisorySummary` struct construction in the diff contains only severity count fields and `total`. No `threshold_applied: true` or `threshold_applied: false` field is present anywhere in the diff. The `summary.rs` model file is not modified to add this field.
