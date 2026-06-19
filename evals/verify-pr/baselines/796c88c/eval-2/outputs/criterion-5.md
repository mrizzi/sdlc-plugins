# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## What was checked

Inspected the PR diff for the presence of a `threshold_applied` boolean field in the response struct (`AdvisorySummary`).

## Evidence

The filtered `AdvisorySummary` struct is constructed in the `Some(threshold)` branch with only these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in the constructed response. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) is not modified in the diff to add this field.

The `None` branch returns the original `summary` as-is, which also would not contain a `threshold_applied` field.

Neither the model definition nor the endpoint handler includes this boolean field anywhere in the diff.

## Verdict: FAIL

The response does not include a `threshold_applied` boolean field. The `AdvisorySummary` struct was not updated to include this field, and neither the filtered nor unfiltered response paths set it. This acceptance criterion is completely unaddressed.
