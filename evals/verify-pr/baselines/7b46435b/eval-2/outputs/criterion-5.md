# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The task requires that the response payload includes a `threshold_applied` boolean field. This field should be `true` when a threshold filter is active and `false` when no threshold is provided, allowing API consumers to programmatically determine whether the returned counts are filtered or complete.

The PR diff does not add a `threshold_applied` field to the `AdvisorySummary` response struct. The filtered response object constructed in the `Some(threshold)` branch contains only:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields are: `critical`, `high`, `medium`, `low`, `total`. There is no `threshold_applied` field.

Similarly, the `None` branch returns the original `summary` object, which also lacks a `threshold_applied` field.

To satisfy this criterion, the implementation would need to:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`)
2. Set `threshold_applied: true` in the filtered response
3. Set `threshold_applied: false` in the unfiltered response (or modify the existing summary to include it)

Neither the `AdvisorySummary` struct modification nor the field assignment appears anywhere in the diff. The model file `modules/fundamental/src/advisory/model/summary.rs` is not modified in this PR.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed `AdvisorySummary`
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the PR diff
- The `AdvisorySummary` struct would need a new `threshold_applied: bool` field
- Both the `Some(threshold)` and `None` branches lack this field
