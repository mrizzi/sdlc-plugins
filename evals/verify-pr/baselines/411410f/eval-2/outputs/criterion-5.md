# Criterion 5: Response includes `threshold_applied` boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

## Detailed Reasoning

The PR does not add a `threshold_applied` boolean field to the response. Examining the diff, the `AdvisorySummary` struct that is returned as JSON contains only the severity count fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

There is no `threshold_applied` field in this struct construction. Additionally, the diff does not show any modification to the `AdvisorySummary` struct definition (located in `modules/fundamental/src/advisory/model/summary.rs` according to the repository structure). The struct would need a new boolean field added to satisfy this criterion.

**What is required:**
1. Add a `threshold_applied: bool` field to the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`
2. Set `threshold_applied: true` when the `Some(threshold)` branch is taken
3. Set `threshold_applied: false` when the `None` branch is taken (or when returning the unfiltered summary)

This field allows API consumers to programmatically determine whether the returned counts are filtered or complete, which is important for correct client-side interpretation of the response.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs` -- no `threshold_applied` field in the constructed `AdvisorySummary`
- File: `modules/fundamental/src/advisory/model/summary.rs` -- not modified in the diff (no struct change)
- The `None` branch returns the unmodified `summary` which would also lack the field
- The word "threshold_applied" does not appear anywhere in the PR diff
