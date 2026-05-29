# Criterion 5: Response includes threshold_applied boolean field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Analysis

The diff constructs the filtered `AdvisorySummary` with these fields:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And for the no-threshold case:

```rust
None => summary,
```

In neither code path is a `threshold_applied` boolean field present. The `AdvisorySummary` struct (defined elsewhere in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) is used as-is without any modification to add a `threshold_applied` field.

The diff does not touch `modules/fundamental/src/advisory/model/summary.rs` at all, which means the `AdvisorySummary` struct was not updated to include the new boolean field.

**What should have been implemented:**

1. The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` should have been extended with a `threshold_applied: bool` field
2. In the filtered path (`Some(threshold) => ...`), `threshold_applied` should be set to `true`
3. In the unfiltered path (`None => ...`), `threshold_applied` should be set to `false`

**Evidence:**
- The `AdvisorySummary` struct construction in the diff includes only: `critical`, `high`, `medium`, `low`, `total` -- no `threshold_applied` field
- The file `modules/fundamental/src/advisory/model/summary.rs` is not modified in the diff
- No boolean field related to threshold status appears anywhere in the diff
- The `None => summary` path returns the original summary unmodified, with no way to include `threshold_applied: false`

This criterion is clearly NOT satisfied. The `threshold_applied` boolean field is entirely absent from the implementation.
