## Criterion 5: Response includes a threshold_applied boolean field

**Criterion**: Response includes a `threshold_applied` boolean field indicating whether filtering is active.

**Result**: FAIL

**Reasoning**:

The diff constructs the filtered `AdvisorySummary` struct with the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in this struct. The `AdvisorySummary` model (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) has not been modified in this diff to include a `threshold_applied: bool` field.

The acceptance criterion explicitly requires a `threshold_applied` boolean that indicates whether threshold filtering is active. This should be `true` when a valid threshold parameter is provided and `false` when no threshold is specified.

Neither the model struct nor the response construction includes this field.

**Verdict**: FAIL -- The `threshold_applied` boolean field is entirely missing from the response. The AdvisorySummary model was not updated and the handler does not set this field.
