## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

### Reasoning

The `AdvisorySummary` struct used in the response does not include a `threshold_applied` boolean field. The diff shows the filtered response is constructed as:

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

The acceptance criterion requires a boolean field that indicates whether threshold filtering is active. This field should be:
- `true` when a threshold parameter is provided (and valid)
- `false` when no threshold parameter is provided

Neither the `AdvisorySummary` struct definition (in `modules/fundamental/src/advisory/model/summary.rs`, which was not modified) nor the endpoint handler adds this field. The struct would need to be modified to include `pub threshold_applied: bool`, and the handler would need to set it to `params.threshold.is_some()` (or similar).

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed response
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff; the `AdvisorySummary` struct was not extended with the new field
- The response JSON will not contain `threshold_applied` in either the filtered or unfiltered case
