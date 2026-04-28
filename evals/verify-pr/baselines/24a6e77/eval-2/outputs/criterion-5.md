# Criterion 5: Response includes threshold_applied boolean field

## Criterion

Response includes a `threshold_applied` boolean field indicating whether filtering is active.

## Verdict: FAIL

## Reasoning

The acceptance criterion explicitly requires that the response body include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field should be:
- `true` when a valid threshold parameter was provided and filtering was applied
- `false` when no threshold parameter was provided

The PR diff does NOT add a `threshold_applied` field to the response. Examining the constructed `AdvisorySummary` struct in the filtering branch:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The struct contains only: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` field.

Furthermore, the diff does not modify the `AdvisorySummary` struct definition (which resides in `modules/fundamental/src/advisory/model/summary.rs` according to the repository structure). To add a `threshold_applied` field, the struct definition would need to be updated with a new `bool` field and that field would need to be set appropriately in both the filtered and unfiltered code paths.

This is a clear gap -- the acceptance criterion is entirely unimplemented.

## Evidence

- The `AdvisorySummary` construction in the diff has exactly 5 fields: `critical`, `high`, `medium`, `low`, `total`
- No `threshold_applied` field appears anywhere in the diff
- The file `modules/fundamental/src/advisory/model/summary.rs` (where `AdvisorySummary` is defined) does not appear in the diff at all, confirming the struct was not modified to include the new field
- The `None` branch returns the original `summary` object, which also lacks a `threshold_applied` field
