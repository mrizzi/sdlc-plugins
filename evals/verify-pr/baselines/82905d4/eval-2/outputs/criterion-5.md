# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result: FAIL**

## Analysis

The PR diff constructs an `AdvisorySummary` struct in the filtered case:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `AdvisorySummary` struct fields included are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field anywhere in the response.

Additionally, the diff for `modules/fundamental/src/advisory/service/advisory.rs` shows no changes to the `AdvisorySummary` struct definition -- it was not modified to add a `threshold_applied` field. The diff for the service file only shows the existing `aggregate_severities` method without any additions.

For this criterion to be satisfied, the implementation would need to:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct (in the model/summary.rs file)
2. Set it to `true` when a threshold parameter is provided and applied
3. Set it to `false` when no threshold is specified

Neither the struct definition nor the endpoint handler includes this field.

**Conclusion:** The `threshold_applied` boolean field is completely absent from the response. This criterion is **not satisfied**.
