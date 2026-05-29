# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

## Analysis

The PR diff constructs the filtered `AdvisorySummary` struct with these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present in this struct are: `critical`, `high`, `medium`, `low`, and `total`. There is NO `threshold_applied` boolean field.

Additionally, looking at the `None` branch:

```rust
None => summary,
```

This returns the unmodified `summary` which also would not contain a `threshold_applied` field unless it was added to the `AdvisorySummary` struct definition.

The PR diff for `modules/fundamental/src/advisory/service/advisory.rs` shows no changes to the `AdvisorySummary` struct definition. The diff only shows the existing aggregation code with no new fields added:

```rust
low: counts.get("low").copied().unwrap_or(0),
total: counts.values().sum(),
```

No `threshold_applied` field is added to either:
1. The `AdvisorySummary` struct definition (in the service layer or model)
2. The response construction in the endpoint handler

**Evidence:**
- No `threshold_applied` field in the `AdvisorySummary` struct construction in `get.rs`
- No changes to the `AdvisorySummary` struct definition in `advisory.rs` or `summary.rs`
- The model file `modules/fundamental/src/advisory/model/summary.rs` is not modified at all in the diff
- The acceptance criterion explicitly requires this field to indicate whether filtering is active

This criterion is NOT satisfied. The `threshold_applied` boolean field is entirely absent from the implementation.
