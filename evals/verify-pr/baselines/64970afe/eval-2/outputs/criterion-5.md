## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Result: FAIL**

### Analysis

The acceptance criterion requires a `threshold_applied` boolean field in the response JSON. This field should be `true` when a valid threshold parameter is provided and filtering is active, and `false` when no threshold is specified.

The diff constructs the response `AdvisorySummary` struct with only the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, `total`. There is no `threshold_applied` field.

### Evidence

1. The `AdvisorySummary` struct is not modified in the diff to add a `threshold_applied: bool` field. The file `modules/fundamental/src/advisory/model/summary.rs` (where `AdvisorySummary` is defined per the repo structure) does not appear in the diff at all.

2. Neither the filtered branch nor the unfiltered branch (`None => summary`) sets or includes a `threshold_applied` value in the response.

3. For this field to work, the `AdvisorySummary` struct definition would need to be updated to include `threshold_applied: bool`, and both branches of the match would need to set it appropriately (`true` when threshold is `Some`, `false` when `None`).

### Impact

API consumers have no way to determine from the response alone whether threshold filtering was applied. This is particularly problematic given that invalid threshold values are silently accepted (criterion 3), meaning a consumer cannot distinguish between "no filter applied" and "invalid filter silently ignored."
