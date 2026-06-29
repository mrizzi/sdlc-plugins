# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Result: FAIL

## Analysis

The diff constructs the filtered `AdvisorySummary` with the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present in the response are: `critical`, `high`, `medium`, `low`, and `total`. There is no `threshold_applied` boolean field anywhere in the constructed response.

Additionally, examining the diff for `modules/fundamental/src/advisory/service/advisory.rs`, no changes were made to the `AdvisorySummary` struct to add a `threshold_applied` field. The service file diff only shows context lines around the existing aggregation logic with no additions.

For the `None` case (no threshold provided), the unmodified `summary` is returned, which also would not contain a `threshold_applied` field.

### What correct implementation would require

1. The `AdvisorySummary` struct (in `modules/fundamental/src/advisory/model/summary.rs`) would need a new `threshold_applied: bool` field
2. The filtered response should set `threshold_applied: true`
3. The unfiltered response should set `threshold_applied: false`

None of these changes are present in the diff.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` in the `AdvisorySummary` construction
- File: `modules/fundamental/src/advisory/service/advisory.rs` -- no structural changes to add the field
- No modifications to `modules/fundamental/src/advisory/model/summary.rs` in the diff at all
- The diff contains zero occurrences of the string "threshold_applied"

## Conclusion

The criterion is not met. The `threshold_applied` boolean field is entirely absent from the implementation. API consumers have no way to determine from the response whether threshold filtering was applied.
