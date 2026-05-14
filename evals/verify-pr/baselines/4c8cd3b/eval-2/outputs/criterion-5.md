# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR does NOT add a `threshold_applied` boolean field to the `AdvisorySummary` response struct. Examining the diff carefully:

In the filtering code, the `AdvisorySummary` struct is constructed with only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field. The `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs`) was not modified in this PR to include the new field.

For this criterion to be met, the implementation would need to:

1. Add `threshold_applied: bool` to the `AdvisorySummary` struct definition in `modules/fundamental/src/advisory/model/summary.rs`
2. Set `threshold_applied: true` when a valid threshold is provided
3. Set `threshold_applied: false` when no threshold is provided (the `None` branch)

Neither the struct modification nor the field assignment appears anywhere in the PR diff.

## Evidence

- File: `modules/fundamental/src/advisory/model/summary.rs` -- NOT modified in the PR diff
- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- the `AdvisorySummary` construction does not include a `threshold_applied` field
- The `None` branch returns the unmodified `summary` which also would not contain the field

## Conclusion

This criterion is NOT met. The `threshold_applied` boolean field is completely absent from both the struct definition and the response construction. Clients have no way to determine from the API response whether threshold filtering was applied.
