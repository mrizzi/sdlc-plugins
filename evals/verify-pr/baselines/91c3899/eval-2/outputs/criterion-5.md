## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Analysis

The diff constructs the response as:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The `AdvisorySummary` struct returned contains only the severity count fields (`critical`, `high`, `medium`, `low`, `total`). There is no `threshold_applied` boolean field anywhere in the response.

The diff does not modify the `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs`) to add a `threshold_applied` field, and the handler does not include any such field in the constructed response.

## Verdict: FAIL

The `threshold_applied` boolean field is completely absent from the response. The `AdvisorySummary` struct was not modified to include this field, and the handler does not set it.
