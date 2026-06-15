# Criterion 5: threshold_applied Boolean Field

**Criterion:** Response includes a `threshold_applied` boolean field indicating whether filtering is active

**Verdict:** FAIL

## Analysis

The `threshold_applied` boolean field is completely absent from the response. The diff shows the `AdvisorySummary` struct being constructed with only the following fields:

- `critical`
- `high`
- `medium`
- `low`
- `total`

There is no `threshold_applied` field defined, set, or returned anywhere in the diff. The acceptance criteria explicitly require this field to indicate whether threshold filtering is active.

When a threshold is provided, the response should include `threshold_applied: true`. When no threshold is provided (backward-compatible mode), it should include `threshold_applied: false`. Neither case is implemented.

## Evidence

From the diff in `get.rs`, the filtered response construction:
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

Neither path includes a `threshold_applied` field. The `AdvisorySummary` struct definition is not modified in this diff to add the field, and the struct construction does not set it.
