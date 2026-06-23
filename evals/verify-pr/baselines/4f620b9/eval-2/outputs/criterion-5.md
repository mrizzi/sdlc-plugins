# Criterion 5: Response includes a threshold_applied boolean field

## Verdict: FAIL

## Reasoning

The acceptance criterion requires that the response includes a `threshold_applied` boolean field indicating whether filtering is active.

### Code Analysis

In `modules/fundamental/src/advisory/endpoints/get.rs`, when filtering is applied, the code constructs an `AdvisorySummary` with these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The constructed struct contains only five fields:
1. `critical`
2. `high`
3. `medium`
4. `low`
5. `total`

There is no `threshold_applied` boolean field in either the filtered or unfiltered response path. The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) has not been modified to include this field.

### Expected Behavior

The response should include:
- `threshold_applied: true` when a valid threshold parameter is provided and filtering is active
- `threshold_applied: false` when no threshold parameter is provided

This allows API consumers to programmatically determine whether the returned counts are filtered or complete.

### Conclusion

The `threshold_applied` boolean field is entirely absent from the response. Neither the `AdvisorySummary` struct nor the handler logic includes this field. This criterion is NOT satisfied.
