# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Analysis

The PR diff constructs the filtered `AdvisorySummary` struct as follows:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields in the constructed `AdvisorySummary` are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Additionally, the `advisory/service/advisory.rs` diff shows no modification to the `AdvisorySummary` struct definition to add a `threshold_applied` field. The diff for that file only shows context lines with no new fields added to the struct.

For the `None` case (no threshold), the original `summary` object is returned directly, which also would not contain a `threshold_applied` field.

The acceptance criterion requires:
- `threshold_applied: true` when a threshold parameter is provided and filtering is active
- `threshold_applied: false` when no threshold parameter is provided

Neither case is handled.

**Conclusion:** The `threshold_applied` boolean field is completely absent from the response. The `AdvisorySummary` struct was not modified to include this field, and the handler does not set it. This criterion is NOT met.
