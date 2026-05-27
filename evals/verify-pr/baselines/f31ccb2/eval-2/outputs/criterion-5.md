## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

### Analysis

The diff does NOT add a `threshold_applied` boolean field to the response. The constructed `AdvisorySummary` in the filtering branch contains only:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

Fields present: `critical`, `high`, `medium`, `low`, `total`. There is no `threshold_applied` field.

Furthermore, the `AdvisorySummary` struct itself (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) was not modified in this diff to add a `threshold_applied: bool` field.

### What should happen

The response should include `threshold_applied: true` when a valid threshold parameter is provided, and `threshold_applied: false` (or the field should be present with value `false`) when no threshold is specified. This would require:

1. Adding `threshold_applied: bool` to the `AdvisorySummary` struct definition
2. Setting it to `true` in the `Some(threshold)` branch
3. Setting it to `false` in the `None` branch (or modifying the existing summary to include it)

Neither step was done. The `AdvisorySummary` model file (`modules/fundamental/src/advisory/model/summary.rs`) does not appear in the diff at all.
