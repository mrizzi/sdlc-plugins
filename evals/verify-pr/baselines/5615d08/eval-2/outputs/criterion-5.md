# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

## Reasoning

The PR diff does **not** add a `threshold_applied` boolean field to the `AdvisorySummary` response struct. Examining the diff:

1. The `AdvisorySummary` struct is not modified anywhere in the diff. The model file `modules/fundamental/src/advisory/model/summary.rs` (where `AdvisorySummary` is defined) does not appear in the diff at all.

2. The filtered `AdvisorySummary` object constructed in `get.rs` contains only the existing fields: `critical`, `high`, `medium`, `low`, and `total`:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied: true` or similar field.

3. The `None` branch simply returns the unmodified `summary`, which also would not have a `threshold_applied` field.

This is a clear omission. The acceptance criterion requires a boolean field in the response that indicates whether threshold filtering is active, allowing API consumers to distinguish between "no counts for this severity" and "severity was filtered out."

## Evidence

- `AdvisorySummary` struct definition (in `model/summary.rs`) is not modified in the diff
- The constructed `AdvisorySummary` in the filtered branch has no `threshold_applied` field
- No new struct or wrapper type is defined to include this field
- The acceptance criterion explicitly requires: "Response includes a `threshold_applied` boolean field indicating whether filtering is active"
