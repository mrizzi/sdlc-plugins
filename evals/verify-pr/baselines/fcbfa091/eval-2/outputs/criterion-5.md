# Criterion 5: Response includes a `threshold_applied` boolean field indicating whether filtering is active

## Verdict: FAIL

## Analysis

The PR does not add a `threshold_applied` boolean field to the response. The `AdvisorySummary` struct is not modified in the diff, and the constructed response object contains only the existing severity count fields.

### Code Under Review

The filtered response construction:

```rust
AdvisorySummary {
    critical: summary.critical,
    high: if threshold_idx <= 1 { summary.high } else { 0 },
    medium: if threshold_idx <= 2 { summary.medium } else { 0 },
    low: if threshold_idx <= 3 { summary.low } else { 0 },
    total: summary.critical + summary.high + summary.medium + summary.low,
}
```

And the unfiltered path:

```rust
None => summary,
```

### Defect: Missing `threshold_applied` field

The `AdvisorySummary` struct (defined in `modules/fundamental/src/advisory/model/summary.rs` per the repository structure) is not modified in this PR diff. The response object only contains the existing fields: `critical`, `high`, `medium`, `low`, `total`.

The acceptance criterion requires a `threshold_applied` boolean field that indicates:
- `true` when a valid threshold parameter was provided and filtering is active
- `false` when no threshold was provided (all severities returned)

This field is completely absent from the implementation.

### Expected Changes

1. Add `threshold_applied: bool` to the `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs`
2. Set `threshold_applied: true` in the `Some(threshold)` branch
3. Set `threshold_applied: false` in the `None` branch (or on the original `summary` before returning)

### Evidence

- The diff for `modules/fundamental/src/advisory/endpoints/get.rs` does not include `threshold_applied` anywhere
- The diff for `modules/fundamental/src/advisory/service/advisory.rs` shows no structural changes to `AdvisorySummary`
- The file `modules/fundamental/src/advisory/model/summary.rs` (where `AdvisorySummary` is defined per repo structure) is not present in the PR diff at all
- A text search for "threshold_applied" across the entire diff yields zero matches
