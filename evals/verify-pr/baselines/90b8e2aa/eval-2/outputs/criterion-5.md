# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The response does not include a `threshold_applied` boolean field. The `AdvisorySummary` struct returned by the endpoint contains only the existing severity count fields and a total.

### Evidence from the Diff

The constructed `AdvisorySummary` in the `Some(threshold)` branch contains:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the `None` branch returns the unmodified `summary`.

Neither branch adds a `threshold_applied` field.

### What Was Required

The task specifies: "Response includes a `threshold_applied` boolean field indicating whether filtering is active."

This would require:
1. Modifying the `AdvisorySummary` struct (likely in `modules/fundamental/src/advisory/model/summary.rs`) to add a `threshold_applied: bool` field.
2. Setting `threshold_applied: true` when a valid threshold is provided.
3. Setting `threshold_applied: false` when no threshold is provided (the `None` branch).

### What Is Missing

- The `AdvisorySummary` struct definition is not modified anywhere in the diff.
- The file `modules/fundamental/src/advisory/model/summary.rs` does not appear in the diff at all.
- No `threshold_applied` field is set in either the `Some` or `None` branch of the handler.

### Conclusion

API consumers have no way to determine from the response alone whether threshold filtering was applied. This field is entirely absent from the implementation.
