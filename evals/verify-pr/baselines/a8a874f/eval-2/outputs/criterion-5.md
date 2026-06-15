# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Reasoning

The diff does NOT add a `threshold_applied` boolean field to the response. Examining the filtering logic in `modules/fundamental/src/advisory/endpoints/get.rs`, the `AdvisorySummary` struct is constructed with only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Furthermore, the `AdvisorySummary` model struct (defined in `modules/fundamental/src/advisory/model/summary.rs` according to the repository structure) is not modified in the diff at all. No changes are made to the model to add a `threshold_applied: bool` field.

For the `None` case (no threshold parameter), the code returns the original `summary` unchanged, which also would lack the `threshold_applied` field.

The acceptance criterion requires:
- When a threshold is provided and active: `threshold_applied: true`
- When no threshold is provided: `threshold_applied: false`

Neither case is handled.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed `AdvisorySummary`
- File: `modules/fundamental/src/advisory/model/summary.rs` -- NOT modified in the diff; the model struct does not include a `threshold_applied` field
- The acceptance criterion is explicitly unmet: the response never contains `threshold_applied`.
