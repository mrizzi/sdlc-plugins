# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The criterion requires that the API response includes a `threshold_applied` boolean field that indicates whether severity filtering is active. This field should be:
- `true` when a valid `threshold` query parameter is provided and filtering is applied
- `false` when no `threshold` parameter is provided (all severities returned)

### What the diff shows

The `AdvisorySummary` struct constructed in the filtered branch contains only these fields:

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

In the unfiltered branch (`None => summary`), the original `summary` object is returned as-is, which also does not include a `threshold_applied` field.

### What is missing

1. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` according to the repository structure) would need a new `threshold_applied: bool` field added.
2. The handler would need to set this field to `true` in the filtered branch and `false` in the unfiltered branch.
3. The diff does not modify `modules/fundamental/src/advisory/model/summary.rs` at all -- this file is not included in the PR changes.

### Impact

Without the `threshold_applied` field, API consumers have no way to determine from the response alone whether filtering was applied. They would need to infer it from the request they sent, which is a weaker contract than an explicit response field.

## Conclusion

This criterion is NOT satisfied. The `threshold_applied` boolean field is completely absent from the response. Neither the model struct nor the handler code includes this field.
