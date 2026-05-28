## Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict: FAIL**

### Evidence

The PR diff in `modules/fundamental/src/advisory/endpoints/get.rs` constructs an `AdvisorySummary` response with the following fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the `None` branch returns the raw `summary` unchanged.

### Analysis

There is **no** `threshold_applied` field anywhere in the PR diff. The response struct `AdvisorySummary` (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repo structure) is not modified in this PR to add a boolean field.

The acceptance criterion explicitly requires:
> "Response includes a `threshold_applied` boolean field indicating whether filtering is active"

This field should be:
- `true` when a valid threshold parameter is provided and filtering is active
- `false` when no threshold parameter is provided

To implement this, the PR would need to:
1. Add `threshold_applied: bool` to the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`
2. Set `threshold_applied: true` in the `Some(threshold)` branch
3. Set `threshold_applied: false` in the `None` branch (or add it to the existing summary)

None of these changes are present. The file `modules/fundamental/src/advisory/model/summary.rs` does not appear in the diff at all, and neither branch of the match expression sets a `threshold_applied` field.

This criterion is definitively not met.
