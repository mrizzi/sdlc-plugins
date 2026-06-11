# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR does not add a `threshold_applied` boolean field to the response. The `AdvisorySummary` struct constructed in the filtering logic contains only the severity count fields and a total:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in this struct construction. The `AdvisorySummary` model (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) is not modified in the diff to add this field.

For the `None` branch (no threshold), the original `summary` is returned as-is, which also would not include a `threshold_applied` field unless the model was updated.

To satisfy this criterion, the implementation would need to:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct (in `model/summary.rs`)
2. Set it to `true` when a valid threshold is provided and filtering is applied
3. Set it to `false` when no threshold is provided

Neither the model modification nor the field assignment exists in the diff.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed `AdvisorySummary`
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (no field added to the struct)
- The acceptance criteria explicitly require this field: "Response includes a `threshold_applied` boolean field indicating whether filtering is active"
