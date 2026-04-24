# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Result: FAIL

## Reasoning

The PR diff does not add a `threshold_applied` boolean field to the response. Examining the constructed `AdvisorySummary` in the filtered case:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The response contains only `critical`, `high`, `medium`, `low`, and `total` fields. There is no `threshold_applied` field.

Additionally, the `AdvisorySummary` struct definition is not modified in this diff (the struct lives in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure). The diff only modifies `get.rs` (endpoint handler) and `advisory.rs` (service), neither of which adds the required boolean field to the response model.

To satisfy this criterion, the implementation would need to:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct (in `model/summary.rs`)
2. Set it to `true` when a valid threshold parameter is provided
3. Set it to `false` when no threshold parameter is provided

This field is entirely absent from the implementation.
