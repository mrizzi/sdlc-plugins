## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

### Verdict: FAIL

### Reasoning

The task requires that the response body includes a `threshold_applied` boolean field that indicates whether threshold filtering is active (true when a threshold parameter is provided, false otherwise).

Examining the diff in `modules/fundamental/src/advisory/endpoints/get.rs`, the `AdvisorySummary` struct being constructed in the filtered response contains only:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

The fields present are: `critical`, `high`, `medium`, `low`, and `total`. There is **no `threshold_applied` field** anywhere in the constructed response.

Furthermore, the `None` branch simply returns `summary` unmodified:

```rust
None => summary,
```

There is no modification to add `threshold_applied: false` to the unfiltered response either.

Checking the diff for `modules/fundamental/src/advisory/service/advisory.rs`, there are no changes to the `AdvisorySummary` struct definition -- the diff shows no additions to the struct. The `AdvisorySummary` model in `modules/fundamental/src/advisory/model/summary.rs` is not modified in this PR at all (the file does not appear in the diff).

**Evidence from the diff:**
- The `AdvisorySummary` struct construction in `get.rs` has 5 fields: `critical`, `high`, `medium`, `low`, `total` -- no `threshold_applied`
- The model file `modules/fundamental/src/advisory/model/summary.rs` is not in the diff, meaning the struct was not extended with a new field
- No occurrence of the string "threshold_applied" appears anywhere in the diff

This criterion is **not satisfied**. The `threshold_applied` boolean field is entirely missing from both the response struct and the response construction logic.
