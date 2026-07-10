## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Verdict: FAIL

### Analysis

The task requires the response to include a `threshold_applied` boolean field that indicates whether threshold filtering is active. This field is completely absent from the implementation.

The diff shows the `AdvisorySummary` struct being constructed with only the existing severity count fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

No `threshold_applied` field is present. The diff also does not modify the `AdvisorySummary` model definition (located at `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) to add this field.

To satisfy this criterion, the implementation would need to:
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct in the model
2. Set it to `true` when a valid threshold parameter is provided
3. Set it to `false` (or omit via `#[serde(skip_serializing_if)]`) when no threshold is provided

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed response
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (no struct field added)
- The response has no way for clients to determine whether filtering was applied
